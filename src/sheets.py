"""
Google Sheets integration for the cryptocurrency tracker.

Loads current worksheet data, updates current prices,
and appends historical price snapshots for each run.
"""

import gspread

from src.config import (
    SPREADSHEET_ID,
    SERVICE_ACCOUNT_FILE,
    CURRENT_SHEET,
    HISTORY_SHEET,
)


def get_sheets():
    """Return worksheets for current market data and historical price records."""
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_key(SPREADSHEET_ID)
    current_ws = sh.worksheet(CURRENT_SHEET)
    history_ws = sh.worksheet(HISTORY_SHEET)
    return current_ws, history_ws


def load_current_data(current_ws):
    """Load existing current-price rows and map them by coin name."""
    values = current_ws.get_all_values()
    existing = {}
    row_map = {}

    for row_index, row in enumerate(values[1:], start=2):
        if not row:
            continue

        row = row + [""] * (4 - len(row))
        coin = row[0].strip()

        if not coin:
            continue

        existing[coin] = {
            "coin": row[0],
            "price": row[1],
            "change_24h": row[2],
            "updated_at": row[3],
        }
        row_map[coin] = row_index

    return existing, row_map


def format_decimal(value: float | None) -> str:
    """Format a decimal value for spreadsheet output."""
    if value is None:
        return ""
    return f"{value:.2f}".replace(".", ",")


def sync_crypto_data(parsed_data: list[dict]):
    """Synchronize fetched cryptocurrency data to current and history sheets."""
    current_ws, history_ws = get_sheets()
    existing, row_map = load_current_data(current_ws)

    current_updates = []
    new_rows = []
    history_rows = []

    updated_count = 0

    for item in parsed_data:
        coin = str(item["coin"]).strip()
        price = format_decimal(item["price"])
        change_24h = format_decimal(item["change_24h"])
        timestamp = str(item["timestamp"]).strip()

        history_rows.append([coin, price, change_24h, timestamp])

        if coin not in existing:
            new_rows.append([coin, price, change_24h, timestamp])
            updated_count += 1
        else:
            row_num = row_map[coin]
            current_updates.append({
                "range": f"A{row_num}:D{row_num}",
                "values": [[coin, price, change_24h, timestamp]],
            })
            updated_count += 1

        icon = "📈" if item["change_24h"] is not None and item["change_24h"] >= 0 else "📉"
        sign = "+" if item["change_24h"] is not None and item["change_24h"] >= 0 else ""
        print(f"{item['symbol']}: {item['price']:.2f} USD ({sign}{item['change_24h']:.2f}%) {icon}")

    if new_rows:
        current_ws.append_rows(
            new_rows,
            value_input_option="USER_ENTERED",
            table_range="A:D",
        )

    if current_updates:
        current_ws.batch_update(
            current_updates,
            value_input_option="USER_ENTERED",
        )

    if history_rows:
        history_ws.append_rows(
            history_rows,
            value_input_option="USER_ENTERED",
            table_range="A:D",
        )

    print("\nRun summary:")
    print(f"- Coins: {len(parsed_data)}")
    print(f"- Updated: {updated_count}")