from typing import List, Optional
from datetime import datetime
import yfinance as yf
from pydantic import BaseModel, Field

class StockPrice(BaseModel):
    symbol: str
    price: float
    currency: str
    timestamp: datetime

class HistoricalData(BaseModel):
    symbol: str
    dates: List[datetime]
    prices: List[float]

def get_stock_price(symbol: str) -> StockPrice:
    """
    Fetch the current stock price for a given symbol.
    """
    ticker = yf.Ticker(symbol)
    # fast_info is often faster than history(period='1d') for current price
    try:
        price = ticker.fast_info['last_price']
        currency = ticker.fast_info['currency']
    except Exception:
        # Fallback
        hist = ticker.history(period="1d")
        if hist.empty:
            raise ValueError(f"Could not fetch data for symbol: {symbol}")
        price = hist['Close'].iloc[-1]
        currency = "USD" # Default assumption if fast_info fails, or fetch metadata

    return StockPrice(
        symbol=symbol.upper(),
        price=price,
        currency=currency,
        timestamp=datetime.now()
    )

def get_historical_data(symbol: str, period: str = "1mo") -> HistoricalData:
    """
    Fetch historical closing prices for a given symbol.
    Args:
        symbol: Stock ticker symbol
        period: Data period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    
    if hist.empty:
        raise ValueError(f"No historical data found for {symbol}")
        
    return HistoricalData(
        symbol=symbol.upper(),
        dates=hist.index.to_pydatetime().tolist(),
        prices=hist['Close'].tolist()
    )

class TechnicalIndicators(BaseModel):
    symbol: str
    sma_20: Optional[float] = None
    ema_20: Optional[float] = None
    rsi_14: Optional[float] = None
    timestamp: datetime

def get_technical_indicators(symbol: str) -> TechnicalIndicators:
    """
    Calculate technical indicators (SMA, EMA, RSI) for a given symbol.
    """
    import pandas as pd
    import pandas_ta as ta # noqa: F401

    ticker = yf.Ticker(symbol)
    # Get enough data to calculate indicators
    df = ticker.history(period="6mo")
    
    if df.empty:
        raise ValueError(f"No data found for {symbol}")

    # Calculate Indicators using pandas_ta
    # SMA 20
    df['SMA_20'] = df.ta.sma(length=20)
    # EMA 20
    df['EMA_20'] = df.ta.ema(length=20)
    # RSI 14
    df['RSI_14'] = df.ta.rsi(length=14)

    latest = df.iloc[-1]
    
    return TechnicalIndicators(
        symbol=symbol.upper(),
        sma_20=latest.get('SMA_20'),
        ema_20=latest.get('EMA_20'),
        rsi_14=latest.get('RSI_14'),
        timestamp=latest.name.to_pydatetime() if hasattr(latest.name, 'to_pydatetime') else datetime.now()
    )
