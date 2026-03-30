# Cryptocurrency Tracker

## Problem
Crypto prices change quickly, and manually checking multiple assets throughout the day makes tracking inefficient.  
Teams, analysts, and business users often need a lightweight way to monitor current prices and keep a simple historical record without building a full analytics platform.

## Solution
Cryptocurrency Tracker is a business-oriented monitoring solution that fetches selected cryptocurrency prices from CoinGecko and synchronizes them to Google Sheets.

It maintains both a current market snapshot and a historical log, making it useful for lightweight reporting, tracking routines, and internal monitoring workflows.

## Features
- Fetches live cryptocurrency prices from CoinGecko
- Tracks 24-hour price change for selected assets
- Supports configurable coin list
- Writes current market state to Google Sheets
- Appends every run to a historical price log
- Uses a simple and lightweight Python architecture
- Centralized configuration in `src/config.py`

## Tech Stack
- Python
- requests
- gspread
- Google Sheets API
- python-dotenv
- CoinGecko API

## Demo Output
```text
BTC: 68420.15 USD (+2.34%) 📈
ETH: 3521.47 USD (-1.12%) 📉

Run summary:
- Coins: 2
- Updated: 2
```

## Setup
Project structure:

```text
cryptocurrency-tracker/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── run.py
│   ├── sheets.py
│   └── tracker.py
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── service_account.json
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
SPREADSHEET_ID=your_google_sheet_id
```

Prepare Google Sheets:
- Create worksheet `current_data`
- Create worksheet `price_history`

Suggested columns for both sheets:
- `coin`
- `price`
- `change_24h`
- `updated_at`

Google Sheets access:
1. Create a Google Cloud project.
2. Enable Google Sheets API.
3. Create a Service Account.
4. Download the JSON key file.
5. Save it as `service_account.json` in the project root.
6. Share the spreadsheet with the service account email as Editor.

Run the tracker:

```bash
python -m src.run
```