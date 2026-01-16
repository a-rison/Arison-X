import pandas as pd
import pandas_ta as ta
from typing import Dict, Any, List
from pydantic import BaseModel

class BacktestResult(BaseModel):
    symbol: str
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    trades: int

class BacktestEngine:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data.
        Data must have datetime index and 'Close' column.
        """
        self.data = data
        self._validate_data()

    def _validate_data(self):
        required_cols = ['Close']
        for col in required_cols:
            if col not in self.data.columns:
                raise ValueError(f"Data must contain {col} column")

    def run_strategy(self, strategy_func) -> pd.Series:
        """
        Run a strategy function that returns a signal series (1 for buy, -1 for sell, 0 for hold).
        """
        # Example: Apply strategy
        self.data['Signal'] = strategy_func(self.data)
        return self.data['Signal']

    def calculate_metrics(self) -> BacktestResult:
        """
        Calculate performance metrics based on Signals.
        Assumes self.data has 'Signal' column.
        """
        if 'Signal' not in self.data.columns:
            raise ValueError("Run a strategy first to generate signals.")

        # Simple vectorized backtest (Market Open/Close assumptions simplified)
        # Daily Return = (Close / Prev Close) - 1
        # Strategy Return = Signal * Daily Return
        
        df = self.data.copy()
        df['Returns'] = df['Close'].pct_change()
        df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns'] # Shift signal to trade next bar

        # Metrics
        from src.backtest.metrics import calculate_sharpe_ratio, calculate_max_drawdown, calculate_total_return

        total_return = calculate_total_return(df['Strategy_Returns'])
        sharpe = calculate_sharpe_ratio(df['Strategy_Returns'])
        max_drawdown = calculate_max_drawdown(df['Strategy_Returns'])

        return BacktestResult(
            symbol="TEST", # Placeholder
            total_return=float(total_return),
            sharpe_ratio=float(sharpe),
            max_drawdown=float(max_drawdown),
            trades=int(df['Signal'].diff().abs().sum() / 2) # Rough trade count
        )

# Example Strategy
def rsi_strategy(df: pd.DataFrame, period=14, low=30, high=70):
    df.ta.rsi(length=period, append=True)
    col_name = f"RSI_{period}"
    
    # 1 where RSI < 30 (Buy), -1 where RSI > 70 (Sell), 0 otherwise? 
    # Or Hold logic? This is a simplified signal for the skeleton.
    signal = pd.Series(0, index=df.index)
    signal[df[col_name] < low] = 1
    signal[df[col_name] > high] = -1
    return signal
