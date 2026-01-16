
from src.tools.market_data import get_stock_price, get_technical_indicators, get_historical_data

def test_market_data():
    symbol = "AAPL"
    print(f"Testing for {symbol}...")
    
    # 1. Price
    try:
        price = get_stock_price(symbol)
        print(f"✅ Price: {price.price} {price.currency}")
    except Exception as e:
        print(f"❌ Price Error: {e}")

    # 2. History
    try:
        hist = get_historical_data(symbol, period="5d")
        print(f"✅ History: Retrieved {len(hist.prices)} data points")
    except Exception as e:
        print(f"❌ History Error: {e}")

    # 3. Technicals
    try:
        tech = get_technical_indicators(symbol)
        print(f"✅ Technicals: RSI={tech.rsi_14}, SMA={tech.sma_20}")
    except Exception as e:
        print(f"❌ Technicals Error: {e}")

if __name__ == "__main__":
    test_market_data()
