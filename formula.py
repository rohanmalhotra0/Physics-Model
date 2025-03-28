# formula.py
import pandas as pd

def get_trade_decision():
    df = pd.read_excel("spy_daily_data.xlsx")
    required_cols = ["close", "SMA50", "SMA30", "MACD", "MACD9", "RSI10", "RSI50"]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")

    df.dropna(subset=required_cols, inplace=True)
    if df.empty:
        raise ValueError("No valid data left after dropping NaNs.")

    latest = df.iloc[-1]

    numBuy, numSell = 0, 0

    if latest["close"] < latest.get("SMA200", float('inf')):
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

    if numBuy > numSell:
        action = "BUY"
    elif numSell > numBuy:
        action = "SELL"
    else:
        action = "HOLD"

    return {
        "action": action,
        "numBuy": numBuy,
        "numSell": numSell,
        "confidence": confidence
    }
