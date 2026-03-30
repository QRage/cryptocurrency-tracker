"""
Application configuration for the cryptocurrency tracker.

Stores tracked assets, display labels, target currency,
and Google Sheets integration settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

COINS = ["bitcoin", "ethereum"]

COIN_LABELS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
}

VS_CURRENCY = "usd"

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = "service_account.json"

CURRENT_SHEET = "current_data"
HISTORY_SHEET = "price_history"