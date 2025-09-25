import requests
import pandas as pd

uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'token' }
response = requests.get(uri, headers=headers)
response = response.json()
matches = response["matches"]
df= pd.DataFrame(matches)