# brokerage.py
import os
from formula import get_trade_decision
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

# Step 1: Get trading signal
decision = get_trade_decision()
action = decision["action"]
numBuy = decision["numBuy"]
numSell = decision["numSell"]
confidence = decision["confidence"]

# Step 2: Alpaca setup
api_key = "PK0OYR5V8WPMEL0794SS"
secret_key = "Os8X7hc4nsnF6YpP15gnUifRgdiwpVYplMkWiKeP"
paper = True

trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper)
account = trade_client.get_account()
print("Account status:", account.status)
print("Equity:", account.equity)
print("Buying power:", account.buying_power)

# Step 3: Prepare trade
symbol = "SPY"
qty = round(0.1 * max(numBuy, numSell), 2)

print(f"\n📊 Strategy Decision: {action}")
print(f"Buy weight: {numBuy}, Sell weight: {numSell}, Confidence: {confidence:.2%}")

# Step 4: If SELL, ensure you're not shorting
if action == "SELL":
    positions = trade_client.get_all_positions()
    owned_qty = 0
    for pos in positions:
        if pos.symbol == symbol:
            owned_qty = float(pos.qty)
    qty = min(qty, owned_qty)

# Step 5: Place trade if valid
if action != "HOLD" and qty > 0:
    order_side = OrderSide.BUY if action == "BUY" else OrderSide.SELL
    order_request = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=order_side,
        type=OrderType.MARKET,
        time_in_force=TimeInForce.DAY,
    )
    order = trade_client.submit_order(order_request)
    print(f"🚀 {action} order submitted for {symbol}, Qty: {qty} (Order ID: {order.id})")
else:
    print("🟡 HOLD — No trade placed (either HOLD signal or insufficient quantity).")
