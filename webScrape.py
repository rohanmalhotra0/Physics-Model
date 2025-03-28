from polygon import RESTClient
import pandas as pd


API_KEY = "G1fpi573K1CupUjoypEIFEEyKFpkwUjw" 
TICKER = "SPY"
START_DATE = "2025-01-01"
END_DATE = "2025-06-13"
FILENAME = "spy_daily_data.xlsx"
SHARES_OUTSTANDING = 929_400_000  

client = RESTClient(api_key=API_KEY)

aggs = []
try:
    for a in client.list_aggs(ticker=TICKER, multiplier=1, timespan="day", from_=START_DATE, to=END_DATE, limit=5000):
        aggs.append({
            "timestamp": pd.to_datetime(getattr(a, "timestamp", getattr(a, "t", None)), unit='ms'),
            "open": a.open,
            "high": a.high,
            "low": a.low,
            "close": a.close,
            "volume": a.volume
        })
except Exception as e:
    print("Error fetching data:", e)
    exit()


df = pd.DataFrame(aggs).sort_values("timestamp")


df["MarketCap"] = df["close"] * SHARES_OUTSTANDING



# SMA
for window in [10, 20, 30, 50, 200]:
    df[f"SMA{window}"] = df["close"].rolling(window=window).mean()

# MACD
df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
df["MACD"] = df["EMA12"] - df["EMA26"]
df["MACD9"] = df["MACD"].ewm(span=9, adjust=False).mean()

# RSI Function
def compute_rsi(data, window):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# RSI for multiple windows
for window in [10, 20, 30, 50, 200]:
    df[f"RSI{window}"] = compute_rsi(df["close"], window)

# Cleanup
df.drop(columns=["EMA12", "EMA26"], inplace=True)


df.to_excel(FILENAME, index=False)
print(f"Exported {len(df)} rows to {FILENAME}")