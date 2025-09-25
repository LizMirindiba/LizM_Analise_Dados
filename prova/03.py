#revisão de dicionário
dict = {
    "nome": "Pedro",
    "idade" : 20,
    "email" : "pedro@pedro.com"
}
#para acessar a chave dentro do dicionário 
dict['email']
dict['nome']


#transformar dicionário em dataframe
import pandas as pd
df = pd.DataFrame([dict])


#chamando API do site: https://viacep.com.br
import requests

cep = '70660011'
url =  f"https://viacep.com.br/ws/{cep}/json/"
response = requests.get(url)
dict_cep = response.json()


#api ipeadata.gov.br
url = 'https://www.ipeadata.gov.br/api/odata4/Metadados'
response = requests.get(url)
metadados = response.json()
metadados['value']
df = pd.DataFrame(metadados)

#acessar código do IBGE
import matplotlib as plt
SERCODIGO = "HOMIC"
url = f"https://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO ='{SERCODIGO}' )"
response = requests.get(url)
dados = response.json()
dados = dados['value']
df = pd.DataFrame(dados)
df.info()
filtro = df['NIVNOME'] == "Brasil"
df_brasil = df.loc[filtro]
df_brasil = [["VALDATA", "VALVALOR"]].plot()