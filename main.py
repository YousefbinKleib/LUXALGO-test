from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    # Example: Handle buy/sell
    if data.get("action") == "buy":
        print("Execute BUY for", data.get("symbol"))
    elif data.get("action") == "sell":
        print("Execute SELL for", data.get("symbol"))

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
