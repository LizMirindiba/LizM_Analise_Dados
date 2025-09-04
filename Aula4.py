#Revisão dicionário 
dic = {
    "Nome":"Liz",
    "Idade": 18,
    "Email": "Liz.mirindiba@.com"
}

#Para acessar as chaves nome, idade e email
dic["Nome"]
dic["Idade"]
dic["Email"]

#tranformar em dataframe 
import pandas as pd 
df = pd.DataFrame([dic])

#API VIACEP.com.br
import requests
url = "https://viacep.com.br/ws/57052480/json/"
response = requests.get(url)
dic_cep = response.json()


url = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url)
metadados = response.json()
metadados = metadados["value"]
df = pd.DataFrame(metadados)

#acessar código do IBGE
SERCODIGO = "HOMIC"
url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"
response = requests.get(url)
dados =response.json()
dados = dados["value"]
df = pd.DataFrame(dados)
df.shape
df.columns
df.info()
df["NIVNOME"]
filtro = df["NIVNOME"] == "Brasil"
df_brasil = df.loc[filtro]
df_brasil[["VALDATA", "VALVALOR"]].plot()