import random

def generate_signals():
    return [
        {"symbol": "AAPL", "signal": random.choice(["BUY", "SELL"])},
        {"symbol": "TSLA", "signal": random.choice(["BUY", "SELL"])},
        {"symbol": "BTC", "signal": random.choice(["BUY", "SELL"])},
    ]