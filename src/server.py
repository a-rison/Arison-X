from mcp.server.fastmcp import FastMCP
from src.tools.market_data import get_stock_price, get_historical_data, StockPrice, HistoricalData

# Initialize FastMCP Server
mcp = FastMCP("Alpha Nexus")

@mcp.tool()
def fetch_price(symbol: str) -> StockPrice:
    """
    Get the current stock price for a given ticker symbol.
    """
    try:
        data = get_stock_price(symbol)
        return data
    except Exception as e:
        return f"Error fetching price for {symbol}: {str(e)}"

@mcp.tool()
def fetch_history(symbol: str, period: str = "1mo") -> HistoricalData:
    """
    Get historical OHLCV data for a ticker.
    Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """
    try:
        data = get_historical_data(symbol, period)
        return data
    except Exception as e:
        return f"Error fetching history for {symbol}: {str(e)}"

if __name__ == "__main__":
    # This runs the server over stdio by default
    mcp.run()
