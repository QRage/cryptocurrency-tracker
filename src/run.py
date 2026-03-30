"""
Main entry point for the cryptocurrency tracker.

Fetches current cryptocurrency market data and syncs it
to Google Sheets for current-state tracking and price history storage.
"""

import os

from dotenv import load_dotenv

from src.tracker import fetch_crypto_data
from src.sheets import sync_crypto_data

load_dotenv()


def validate_env():
    """Validate required environment variables before application startup."""
    required_vars = ["SPREADSHEET_ID"]
    missing = [name for name in required_vars if not os.getenv(name)]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


def main():
    """Run one full synchronization cycle for tracked cryptocurrencies."""
    validate_env()
    data = fetch_crypto_data()
    sync_crypto_data(data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")