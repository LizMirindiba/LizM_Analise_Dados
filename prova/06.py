"""
objetivo: ganhar dinheiro investindo nas melhores ações da B3
coletar dados do balanço 2025 2º tri
Limpar e organinzar os dados

"""

#código para a prova

import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDAzNzc3LCJpYXQiOjE3NTY4MTE3NzcsImp0aSI6IjA5ODAyNTZjN2ZlNjQ1YjJiZGM0YjVmYTdiZDYxM2NmIiwidXNlcl9pZCI6IjQyIn0.ZhBi4CDm0W2b8pQyrDKyeXfqn5mFdmAu1xh1WFMBxgQ"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'data_base': '2025-09-01'
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df['setor'] == 'construção'
tickers = df.loc[filtro, 'ticker'].values
lista_resultado = []

#inicio do loop for

for ticker in ["PETR4", "VALE3", "BBAS3"]:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T'
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response['dados'][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    #lucro liquido
    filtro = (
        (df["conta"]== "3.11")&
        (df["descricao"].str.contains("^lucro", case = False))&
        (df["data_ini"] == "2025-01-01")
    )

    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

    #PL
    filtro = (
        (df["conta"].str.contains("2.0", case=False))&
        (df["descricao"].str.contains("^patrim", case = False))
    )

    pl = df.loc[filtro, ["valor"]].iloc[0]

    #ROE
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
        "ticker": ticker,
        "roe" : roe
    }
    lista_resultado.append(resultados)
    print(ticker, roe)

df_final = pd.DataFrame(lista_resultado)
df_final.sort_values(["roe"])

"""

calcular o ROIC para aula do dia 04/09

roe = lucro liquido / patrimonio liquido
roic = ebit / valor investido
ebit = lucro operacional
3.05 = resultado antes do resultado financeiro e dos tributos
valor investido = capital proprio + capital de terceiro
capital terceiros = emprestimos
2.01.04 = emprestimos e financeiro
capital proprio = pl


"""


