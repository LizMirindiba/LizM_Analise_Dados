import pandas as pd
df= pd.read_csv("//Users//lizmirindiba//Library//Mobile Documents//com~apple~CloudDocs//Liz_analise_dados//imoveis_brasil.csv")
df.shape
df.columns
df.head()
df.tail(5)
df.sample(5)
df.info()

#verificar os tipos de imóveis 
df["Tipo_Imovel"].unique()

# Imoveis com valores maiores que 1M
filtro = df["Valor_Imovel"] > 1000000
df_1M = df.loc[filtro]

#Selecionar Cidade, bairro, valor e gravar no df2
colunas_selecionadas = ["Cidade", "Bairro", "Valor_Imovel"]
df2=df[colunas_selecionadas]

#Ordenar os valores dos imóveis
df.sort_values(["Valor_Imovel"], ascending=False)

#Valor médio dos imóveis
valor_medio_geral= df["Valor_Imovel"].mean()

#Valor médio dos imóveis de curitiba
filtro = df["Cidade"] == "Curitiba"
Valor_médio = df.loc[filtro, ["Valor_Imovel"]].mean()
Valor_médio

#Valores acima do valor médio
valor_medio_geral
filtro = df["Valor_Imovel"] > 2491564.81
df_maior = df.loc[filtro]
len(df_maior)

#Valores abaixo do valor médio
valor_medio_geral
filtro = df["Valor_Imovel"] < 2491564.81
df_menor = df.loc[filtro]
len(df_menor)