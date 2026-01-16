
import pandas as pd
from src.tools.market_data import get_historical_data
from src.backtest.engine import BacktestEngine, rsi_strategy

def test_engine():
    symbol = "NVDA"
    print(f"Fetching data for {symbol}...")
    
    try:
        # Get data properly formatted for engine
        hist = get_historical_data(symbol, period="1y")
        
        # Convert List[datetime] and List[float] to DataFrame
        df = pd.DataFrame({
            'Close': hist.prices
        }, index=pd.DatetimeIndex(hist.dates))
        
        print(f"Data fetched: {len(df)} candles.")
        
        # Initialize Engine
        engine = BacktestEngine(df)
        
        # Run Strategy
        print("Running RSI Strategy...")
        engine.run_strategy(rsi_strategy)
        
        # Calculate Metrics
        results = engine.calculate_metrics()
        results.symbol = symbol
        
        print("\n=== Backtest Results ===")
        print(f"Symbol: {results.symbol}")
        print(f"Total Return: {results.total_return:.2%}")
        print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
        print(f"Max Drawdown: {results.max_drawdown:.2%}")
        print(f"Trades Executed: {results.trades}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine()
