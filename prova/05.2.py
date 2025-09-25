#Planilhao
import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3MDAwLCJpYXQiOjE3NTg2MjUwMDAsImp0aSI6ImE1MTcyNDFkMjVmMTQzNjE5NmUwZGQ4MjNmNzQwYzYzIiwidXNlcl9pZCI6IjQyIn0.hkjJt-zo7NI3Q_jn6USXVM5bKpdJ0P4ivwuQYzBIGQw"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'data_base': '2025-09-01'}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df["setor"]=="construção"
tickers = df.loc[filtro, "ticker"].values
lista_resultado = []
lista_resultado2= []
# Inicio do for loop
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
    # Lucro Operacional
    filtro = (
           (df["conta"]=="3.05") &
           (df["descricao"].str.contains("^resultado antes", case=False)) &
          (df["data_ini"]=="2025-01-01")
            )
    lucro_operacional = df.loc[filtro, ["valor"]].iloc[0]
   # PL
    filtro = (
           (df["conta"].str.contains("2.0.", case=False)) &
           (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]

    #Emprestimos
    filtro = (
            (df["conta"].str.contains("2.01.04", case=False)) &
            (df["descricao"].str.contains("^empr.stimos", case=False))
            )
    emprestimos = df.loc[filtro, ["valor"]].iloc[0]
   #ROIC
    roic = lucro_operacional / (emprestimos+pl)
    roic = roic.iloc[0]
    resultados = {
                "ticker":ticker,
                "roic": roic
        }
    lista_resultado.append(resultados)
    print(ticker, roic)

   #ROE
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
        "ticker":ticker, 
        "roe":roe

    }
    lista_resultado2.append(resultados)
    print(ticker, roe)
df_roic = pd.DataFrame(lista_resultado)
df_roe = pd.DataFrame(lista_resultado2)
df_final = pd.merge(df_roic,df_roe)
#Cria uma coluna de media
df_final["media"] = (df_final["roic"] + df_final["roe"] / 2)
df_final.sort_values("media")