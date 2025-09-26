# src/client.py
import os
from binance.client import Client
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize Binance Futures Testnet client
client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

def get_client():
    return client
