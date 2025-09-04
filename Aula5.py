import pandas as pd 
file = "//Users//lizmirindiba//Library//Mobile Documents//com~apple~CloudDocs//Liz_analise_dados//cadastro_alunos.xlsx"
df = pd.read_excel(file)
filtro = df["nome_aluno"].str.contains("^liz|ana", regex=True,case=False)
df.loc[filtro]

import requests
import pandas as pd 
url = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url)
metadados = response.json
metadados = metadados["Value"]
df = pd.DataFrame(metadados)
df["SERNOME"]


import requests
import json

uri = 'https://api.football-data.org/v4/teams'
headers = { 'X-Auth-Token': 'd4092b30a7e14743800f39089c27f7b5' }
response = requests.get(uri, headers=headers)
response = response.json()
teams = response["teams"]
df = pd.DataFrame(teams)
df