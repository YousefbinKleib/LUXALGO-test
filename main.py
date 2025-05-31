import os
import json
from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP

app = Flask(__name__)

# Load API keys from environment variables
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook data:", data)

    try:
        action = data.get("action")
        symbol = data.get("symbol", "BTCUSDT")
        leverage = 10  # ثابت دائمًا

        # Get wallet balance
        wallet_info = session.get_wallet_balance(accountType="UNIFIED")
        usdt_balance = float(wallet_info["result"]["list"][0]["totalEquity"])
        print("USDT Balance:", usdt_balance)

        # Get market price
        price_info = session.get_ticker(category="linear", symbol=symbol)
        last_price = float(price_info["result"]["lastPrice"])
        print("Market Price:", last_price)

        # Calculate position size based on 10% of balance * leverage
        position_usdt = (usdt_balance * 0.10) * leverage
        quantity = round(position_usdt / last_price, 3)

        # Set leverage
        session.set_leverage(category="linear", symbol=symbol, buy_leverage=leverage, sell_leverage=leverage)

        # Place market order
        side = "Buy" if action == "long" else "Sell"
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=quantity,
            time_in_force="GoodTillCancel"
        )

        return jsonify({"status": "success", "order": order}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
