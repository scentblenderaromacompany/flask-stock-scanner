import numpy as np
import pandas as pd
from yfinance import Ticker

def simple_portfolio_summary(stocks):
    """
    A simplified function to analyze the portfolio.
    It provides basic stats like average returns and standard deviation for each stock.
    """
    data = {stock: Ticker(stock).history(period="1y")['Close'] for stock in stocks}
    df = pd.DataFrame(data)

    # Calculate daily returns
    returns = df.pct_change()

    # Compute average return and risk (std dev)
    summary = {
        'average_return': returns.mean() * 252,  # Annualized average return
        'risk': returns.std() * np.sqrt(252)  # Annualized risk (standard deviation)
    }

    return summary
