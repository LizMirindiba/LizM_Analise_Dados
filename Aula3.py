import pandas as pd
arquivo = "//Users//lizmirindiba//Library//Mobile Documents//com~apple~CloudDocs//Liz_analise_dados//titanic.csv"
df = pd.read_csv(arquivo)
df
df.shape
df.columns
df.info()
#encontrar valores vazios e somar esses dados!
df.isna().sum()
#Linhas com valores de Fare vazias (filtro)
filtro = df ["Fare"].isna()
df.loc[filtro]
#Linhas com valores de Age vazias (filtro)
filtro = df ["Age"].isna()
df.loc[filtro]
média_idade= df["Age"].mean()
df["Age"] = df["Age"].fillna(0)
#Calcular média dos homens
filtro = df ["Sex"]== "male"
df_homem = df.loc[filtro]
df_homem["Age"].mean()
#Calcular média mulheres
filtro = df ["Sex"] == "female"
df_mulher = df.loc[filtro]
df_mulher["Age"].mean()
#Groupby
df.groupby("Sex")["Age"].max()
df.groupby("Sex")["Age"].mean()
#Filtrar por duas colunas 
filtro = (df["Sex"]=="male") & (df["Survived"]== 1)
df_h_sobreviv = df.loc[filtro]
df_h_sobreviv
#Mulheres sobreviventes
filtro = (df["Sex"]=="female") & (df["Survived"]== 1)
df_f_sobreviv = df.loc[filtro]
df_f_sobreviv
#Criar uma nova coluna de "FamilyMembers"
df["FamilyMembers"] = df["SibSp"] + df["Parch"] + 1 
df