import brokerage as brk
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
import alpaca_trade_api as tradeapi
import time

if __name__ == "__main__":
    # Step 1: Get trading signal
    decision = brk.get_trade_decision()
    action = decision["action"]
    numBuy = decision["numBuy"]
    numSell = decision["numSell"]
    confidence = decision["confidence"]

    # Step 2: Alpaca setup (consider storing keys securely!)
    api_key = "PK0OYR5V8WPMEL0794SS"
    secret_key = "Os8X7hc4nsnF6YpP15gnUifRgdiwpVYplMkWiKeP"
    paper = True

    trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper)
    account = trade_client.get_account()

    print("Account status:", account.status)
    print("Equity:", account.equity)
    print("Buying power:", account.buying_power)
    symbol = "SPY"

    # Get the final quantity based on the strategy decision
    qty = brk.make_trade_decision(trade_client, symbol, action, numBuy, numSell, confidence)

    if qty is not None:
        # Step 3: Execute the trade
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if action == "BUY" else OrderSide.SELL,
            type=OrderType.MARKET,
            time_in_force=TimeInForce.DAY
        )

        try:
            order_response = trade_client.submit_order(order_data)
            print(f"✅ Order submitted: {order_response}")
        except Exception as e:
            print(f"❌ Error submitting order: {e}")
    