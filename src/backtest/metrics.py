
import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Calculate annualized Sharpe Ratio.
    """
    if returns.std() == 0:
        return 0.0
    return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

def calculate_max_drawdown(returns: pd.Series) -> float:
    """
    Calculate Maximum Drawdown from peak.
    """
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def calculate_total_return(returns: pd.Series) -> float:
    """
    Calculate cumulative total return.
    """
    return (1 + returns).prod() - 1

def calculate_volatility(returns: pd.Series) -> float:
    """
    Calculate annualized volatility.
    """
    return returns.std() * np.sqrt(252)
