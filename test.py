import requests
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "scholarly/author/Marty Banks")
print(response.json())
print('\n')
response = requests.get(BASE + "scholarly/pub/A density-based algorithm for discovering clusters in large spatial databases with noise")

print(response.json())