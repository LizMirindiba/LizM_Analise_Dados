# 1 - Vocˆ tem acesso … API do Laborat¢rio de Finan‡as, que fornece dados do Planilh?o em formato JSON. 
# A autentica‡?o ‚ feita via JWT Token no cabe‡alho da requisi‡?o.
# Acesse a API no endpoint: https://laboratoriodefinancas.com/api/v1/planilhao
# passando como parƒmetro a data do dia de hoje (por exemplo, "2025-09-17").
# Construa um DataFrame pandas a partir dos dados recebidos.
# Selecione a empresa que apresenta o maior ROE (Return on Equity) nessa data.
# Exiba o nome da empresa e o valor do ROE correspondente.

import pandas as pd 
import requests
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-17'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
df.columns

#uma função para achar o maior id
empresa_maior_roe = df.loc[df['roe'].idxmax()]

###outra maneira
maior_roe_valor = df['roe'].max()
empresa_maior_roe = df.loc[df['roe'] == maior_roe_valor].iloc[0]
ticker = empresa_maior_roe['ticker']
valor_roe = empresa_maior_roe['roe']

#outra maneira
roe_max = df["roe"].max()
filtro = df["roe"] == roe_max
df.loc[filtro]

#usando sort values
colunas = ["ticker", "roe"]
df[colunas].sort_values("roe", ascending=False)

# 2 - Acesse a API do Planilh?o e traga os dados de uma data de sua escolha.
# Construa um DataFrame pandas com os dados recebidos.
# Filtre as empresas que pertencem ao setor ?petr¢leo?.
# Elimine todos os registros cujo indicador P/VP (p_vp) seja negativo.
# Selecione a empresa com o maior P/VP dentro do setor de petr¢leo e exiba seu ticker, setor e valor de P/VP.
import pandas as pd 
import requests
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-17'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = (df["setor"] == 'petróleo') & (df["p_vp"]>0)
colunas = ["ticker", "setor", "p_vp"]
df =df[colunas]
df[filtro].nlargest(1, "p_vp")
#usando sort values
df[filtro].sort_values("p_vp", ascending=False)


# 3 - A API do Laborat¢rio de Finan‡as fornece informa‡?es de balan‡os patrimoniais de empresas listadas na B3.
# Acesse o endpoint: https://laboratoriodefinancas.com/api/v1/balanco
# usando o ticker PETR4 e o per¡odo 2025/2§ trimestre (ano_tri = "20252T").
# O retorno da API cont‚m uma chave "balanco", que ‚ uma lista com diversas contas do balan‡o.
# Localize dentro dessa lista a conta cuja descri‡?o ‚ ?1 - Ativo Total?.
# Exiba o valor correspondente a essa conta.

import requests
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'PETR4', 
'ano_tri': '20231T'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

dados = response.json()["dados"][0]
dados = dados["balanco"]
df = pd.DataFrame(dados)
filtro = (df["descrição"] == "Ativo Total") & (df["conta"] == "1")
df.loc[filtro]["valor"].iloc[0]