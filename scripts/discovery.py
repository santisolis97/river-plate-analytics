import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SOCCER_API_KEY")

# 1. Primero buscamos el ID de Argentina
def find_argentina_leagues():
    url = f"https://api.soccerdataapi.com/league/?auth_token={API_KEY}"
    headers = {'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    leagues = response.json().get('results', [])
    
    print("--- Ligas en Argentina ---")
    for league in leagues:
        if league['country']['name'].lower() == 'argentina':
            print(f"ID: {league['id']} | Nombre: {league['name']}")

if __name__ == "__main__":
    find_argentina_leagues()