import pandas as pd
import alpaca_trade_api as tradeapi

# Alpaca Credentials
api_key = "PK0OYR5V8WPMEL0794SS"
secret_key = "Os8X7hc4nsnF6YpP15gnUifRgdiwpVYplMkWiKeP"
paper = True
BASE_URL = "https://paper-api.alpaca.markets"  # use the paper trading URL

api = tradeapi.REST(api_key, secret_key, BASE_URL)

def get_trade_decision():
    df = pd.read_excel("spy_daily_data.xlsx")
    required_cols = ["close", "SMA50", "SMA30", "MACD", "MACD9", "RSI10", "RSI50", "SMA200"]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")

    df.dropna(subset=required_cols, inplace=True)
    if df.empty:
        raise ValueError("No valid data left after dropping NaNs.")

    latest = df.iloc[-1]

    numBuy, numSell = 0, 0

    if latest["close"] < latest["SMA200"]:
        numBuy += 2
    else:
        numSell += 1

    if latest["close"] < latest["SMA50"]:
        numBuy += 1
    else:
        numSell += 0.5

    if latest["close"] < latest["SMA30"]:
        numBuy += 0.05
    else:
        numSell += 0.025

    if latest["MACD"] < latest["MACD9"]:
        numBuy += 0.5
    else:
        numSell += 0.25

    if latest["RSI10"] < 30:
        numBuy += 0.5
    else:
        numSell += 0.25

    if latest["RSI50"] < 30:
        numBuy += 1
    else:
        numSell += 0.5

    confidence = abs(numBuy - numSell) / max((numBuy + numSell), 1)

    account = api.get_account()
    buying_power = float(account.buying_power)

    # Determine trade size based on confidence
    trade_fraction = min(confidence, 1)  # cap at 100% of buying power

    if numBuy > numSell:
        action = "BUY"
        trade_amount = buying_power * trade_fraction
    elif numSell > numBuy:
        action = "SELL"
        position = api.get_position("SPY") if api.list_positions() else None
        trade_amount = float(position.market_value) * trade_fraction if position else 0
    else:
        action = "HOLD"
        trade_amount = 0

    return {
        "action": action,
        "numBuy": numBuy,
        "numSell": numSell,
        "confidence": confidence,
        "trade_amount": trade_amount
    }