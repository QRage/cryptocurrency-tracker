"""
Cryptocurrency market data fetching utilities.

Requests current prices and 24-hour price changes from CoinGecko
for the configured set of tracked assets.
"""

from datetime import datetime, UTC

import requests

from src.config import COINS, COIN_LABELS, VS_CURRENCY

API_URL = "https://api.coingecko.com/api/v3/simple/price"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_crypto_data() -> list[dict]:
    """Fetch current cryptocurrency prices and 24-hour changes."""
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": VS_CURRENCY,
        "include_24hr_change": "true",
    }

    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    data = response.json()

    timestamp = datetime.now(UTC).isoformat()
    rows = []

    for coin in COINS:
        coin_data = data.get(coin, {})
        price = coin_data.get(VS_CURRENCY)
        change_24h = coin_data.get(f"{VS_CURRENCY}_24h_change")

        rows.append({
            "coin": coin,
            "symbol": COIN_LABELS.get(coin, coin.upper()),
            "price": round(float(price), 2) if price is not None else None,
            "change_24h": round(float(change_24h), 2) if change_24h is not None else None,
            "timestamp": timestamp,
        })

    return rows