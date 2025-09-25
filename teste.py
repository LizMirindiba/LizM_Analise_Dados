import matplotlib.pyplot as plt

# Dados dos ciclos
anos = ['1996', '1997']
ciclo_operacional = [109, 181]
ciclo_financeiro = [62, 112]

# Criação do gráfico
plt.figure(figsize=(8, 5))
plt.plot(anos, ciclo_operacional, marker='o', label='Ciclo Operacional')
plt.plot(anos, ciclo_financeiro, marker='s', label='Ciclo Financeiro')
plt.title('Evolução dos Ciclos (1996-1997)')
plt.xlabel('Ano')
plt.ylabel('Dias')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()  


import requests
import pandas as pd

def fetch_data(endpoint):
    response = requests.get(f"https://rickandmortyapi.com/api/{endpoint}")

    if response.status_code == 200:
        return response.json()
    else:
        return None

characters_data = fetch_data("character")

if characters_data:
    characters_list = characters_data.get("results")
    if characters_list:
        print(characters_list)
    else:
        print('Não foi possível encontrar a lista de personagens.')
else:
    print('Falha ao conectar à API.')



import pandas as pd
import requests

#para vários personagens
api = "https://rickandmortyapi.com/api/character"

#personagens espeficicos basta colocar o id no final da url
api = "https://rickandmortyapi.com/api/character/100"

# Make the request and convert the response to a dictionary
response = requests.get(api)
dados = response.json()

#A chave "results" não é um local físico no código. 
# Ela é uma das chaves que compõem o objeto JSON que a API do Rick and Morty te retorna
lista_de_personagens = dados.get("results")

#para retornar um personagem especifico pq o personagem é tratado como uma lista
lista_de_personagens = [dados]

# Now create the DataFrame from the extracted list
df = pd.DataFrame(lista_de_personagens)

print(df.head())