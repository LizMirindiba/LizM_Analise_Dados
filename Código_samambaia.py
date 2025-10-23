from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import re
import requests
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import folium
import rpy2.robjects as ro
from geopy.distance import geodesic
from rpy2.robjects import pandas2ri, conversion

# Configuracoes do navegador
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()

# Acessa o site
url = 'https://www.dfimoveis.com.br/'
driver.get(url)
wait = WebDriverWait(driver, 10)

# Parametros de pesquisa
tipo = "VENDA"
tipos = "TODOS"
estado = "DF"
cidade = "SAMAMBAIA"
# quartos = "2"

# Funcao para preencher filtros
def preencher_filtro(by, value, texto):
    element = wait.until(EC.element_to_be_clickable((by, value)))
    element.click()
    search_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
    search_field.send_keys(texto)
    search_field.send_keys(Keys.ENTER)

preencher_filtro(By.ID, 'select2-negocios-container', tipo)
preencher_filtro(By.ID, 'select2-tipos-container', tipos)
preencher_filtro(By.ID, 'select2-estados-container', estado)
preencher_filtro(By.ID, 'select2-cidades-container', cidade)

# Selecao de quartos
# element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-quartos-container')))
# element.click()
# sleep(2)
# opcoesQuartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'select2-results__option')))
# for opcao in opcoesQuartos:
#     if opcao.text.strip() == quartos:
#         opcao.click()
#         break

# Busca imoveis
wait.until(EC.element_to_be_clickable((By.ID, "botaoDeBusca"))).click()

lst_imoveis = []
while True:
    resultado = wait.until(EC.presence_of_element_located((By.ID, "resultadoDaBuscaDeImoveis")))
    elementos = resultado.find_elements(By.TAG_NAME, 'a')

    for elem in elementos:
        try:
            imovel = {
                'endereco': elem.find_element(By.CLASS_NAME, 'ellipse-text').text,
                'preco': elem.find_element(By.CLASS_NAME, 'body-large.bold').text
            }
            lst_imoveis.append(imovel)
        except:
            continue

    botao_proximo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.btn.next')))
    if "disabled" in botao_proximo.get_attribute("class"):
        print("Última página alcançada.")
        break

    driver.execute_script("arguments[0].click();", botao_proximo)
    sleep(2)

driver.quit()

# Limpeza e padronização dos dados
df = pd.DataFrame(lst_imoveis)

# Converte preço para número
df["preco"] = pd.to_numeric(
    df["preco"].str.extract(r"(\d[\d\.,]*)")[0].str.replace(".", "").str.replace(",", "")
)

# Padroniza endereços
df["endereco"] = df["endereco"].str.upper()
df["endereco"] = df["endereco"].apply(
    lambda x: x if "SAMAMBAIA" in x else f"{x}, SAMAMBAIA SUL, SAMAMBAIA"
)

# Extrai padrão de endereço válido
padrao_endereco = r"(Q[RN]\s?\d{3}(?:\s?CONJUNTO\s?\d+)?(?:,\s?SAMAMBAIA (?:SUL|NORTE), SAMAMBAIA)?)"
df["endereco"] = df["endereco"].str.extract(padrao_endereco)
df = df.dropna(subset=["endereco"])

# Salva CSV inicial
df.to_csv("imoveis_samambaia.csv", index=False, encoding="utf-8")

# Limpeza adicional de endereço
df["endereco"] = df["endereco"].str.replace(r",\s?\d+[\.,]?\d*", "", regex=True)
df.to_csv("imoveis_samambaia_corrigido.csv", index=False, encoding="utf-8")

# Recarrega dados corrigidos
df = pd.read_csv("imoveis_samambaia_corrigido.csv")

# Função de geocodificação
def geocodificar_nominatim(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": endereco,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
        "countrycodes": "br"
    }
    headers = {"User-Agent": "ProjetoImoveisSamambaia/1.0"}
    try:
        resposta = requests.get(url, params=params, headers=headers).json()
        if resposta:
            return float(resposta[0]["lat"]), float(resposta[0]["lon"])
    except Exception as e:
        print(f"Erro ao geocodificar {endereco}: {e}")
    return None, None

# Aplica geocodificação
df["lat"], df["lng"] = zip(*df["endereco"].apply(lambda x: geocodificar_nominatim(x)))
sleep(1)

# Filtra imóveis com coordenadas válidas
df_localizados = df.dropna(subset=["lat", "lng"]).copy()

# Calcula distância até estação de metrô central
metro_coords = (-15.8755, -48.0601)  # Estação Samambaia
df_localizados["distancia_metro_km"] = df_localizados.apply(
    lambda row: geodesic((row["lat"], row["lng"]), metro_coords).km, axis=1
)

# Salva CSV final com coordenadas
df_localizados.to_csv("imoveis_samambaia_cordenadas_corrigido.csv", index=False, encoding="utf-8")

# Visualizacao das analises 
## Analise 1 - Regressao linear simples 
X = df_localizados["distancia_metro_km"]
y = df_localizados["preco"]

# Adiciona constante (intercepto)
X_const = sm.add_constant(X)
modelo = sm.OLS(y, X_const).fit()
print(modelo.summary())
