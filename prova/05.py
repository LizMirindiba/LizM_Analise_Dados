####  Petrobras  ####
import requests
import pandas as pd 
#Pegar o token na area access no site
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
#ticker é a  sigla da empresa que eu quero
params = {
'ticker': 'PETR4',
'ano_tri': '20252T',
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)
df.columns
df.shape
#Lucro Liquido
filtro= (
    (df["conta"] == "3.11") & 
    (df["descricao"].str.contains("^lucro", case=False)) &
    (df["data_ini"]=="2025-01-01")
    )

lucro_liquido = df.loc[filtro,["valor"]].iloc[0]
#Patrimonio liquido
filtro2= (
    (df["conta"] == "2.03") & 
    (df["descricao"].str.contains("^patrim.nio", case=False))
    )
patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]
roe = lucro_liquido / patrimonio_liquido
roe
####  VALE ####
import requests
import pandas as pd 
#Pegar o token na area access no site
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
#ticker é a  sigla da empresa que eu quero
params = {
'ticker': 'VALE3',
'ano_tri': '20252T',
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)
df.columns
df.shape
#Lucro Liquido
filtro= (
    (df["conta"] == "3.11") & 
    (df["descricao"].str.contains("^lucro", case=False)) &
    (df["data_ini"]=="2025-01-01")
    )
lucro_liquido = df.loc[filtro,["valor"]].iloc[0]
#Patrimonio liquido
filtro2= (
    (df["conta"] == "2.03") & 
    (df["descricao"].str.contains("^patrim.nio", case=False))
    )
patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]
roe = lucro_liquido / patrimonio_liquido
roe
# criar um for loop
for ticker in ["PETR4", "VALE3", "BBAS3"]:
    params = {
    'ticker': ticker,
    'ano_tri': '20252T',
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
    df.columns
    df.shape
    #Lucro Liquido
    filtro= (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )
    lucro_liquido = df.loc[filtro,["valor"]].iloc[0]
    #Patrimonio liquido
    filtro2= (
        (df["conta"].str.contains("2.0.", case=False)) & 
        (df["descricao"].str.contains("^patrim.nio", case=False))
        )

    patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]
    roe = lucro_liquido / patrimonio_liquido
    print(roe)
#Planilhão
import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'data_base': '2025-01-09'}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df["setor"]=="construção"
tickers = df.loc[filtro, "ticker"].values
#Inicio do loop
lista_resultado=[]
for ticker in tickers:
    params = {
    'ticker': ticker,
    'ano_tri': '20252T',
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
    #Lucro Liquido
    filtro= (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )
    lucro_liquido = df.loc[filtro,["valor"]].iloc[0]
    #Patrimonio liquido
    filtro= (
        (df["conta"].str.contains("2.0.", case=False)) & 
        (df["descricao"].str.contains("^patrim", case=False))
        )
    pl = df.loc[filtro,["valor"]].iloc[0]
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
        "ticker":ticker, 
        "roe":roe

    }
    lista_resultado.append(resultados)
    print(ticker, roe)
df_final= pd.DataFrame(lista_resultado)
df_final.sort_values(["roe"])

#roe=Lucro Líq/Patrim Líq
#roic=ebit/valor investido
#ebit=lucro operacional
#Valor investido = capital próprio (PL) + capital de terceiros (empréstimos)