import pandas as pd

df = pd.read_excel("spy_daily_data.xlsx")

# If you added SMA200, include it; if not, remove it
required_cols = ["close", "SMA50", "SMA30", "MACD", "MACD9", "RSI10", "RSI50"]

# Only keep rows with all required indicators
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise KeyError(f"Missing required columns: {missing_cols}")

df.dropna(subset=required_cols, inplace=True)

if df.empty:
    raise ValueError("No valid data left after dropping NaNs.")

latest = df.iloc[-1]

# Strategy logic
numBuy = 0
numSell = 0

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

# Final decision
confidence = abs(numBuy - numSell) / max((numBuy + numSell), 1)

if numBuy > numSell:
    action = "BUY"
    print(f"📈 Action: {action} — Buy {round(0.1 * numBuy * 100, 2)}% of portfolio (confidence: {confidence:.2%})")
elif numSell > numBuy:
    action = "SELL"
    print(f"📉 Action: {action} — Sell {round(0.1 * numSell * 100, 2)}% of portfolio (confidence: {confidence:.2%})")
else:
    print("🤝 Action: HOLD — No clear signal today.")

print(f"\nBreakdown → Buy: {numBuy}, Sell: {numSell}, Confidence: {confidence:.2%}")
