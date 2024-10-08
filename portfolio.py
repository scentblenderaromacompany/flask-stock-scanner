import numpy as np
import pandas as pd
from yfinance import Ticker
from sklearn.covariance import LedoitWolf

def optimize_portfolio(stocks):
    """
    Use mean-variance optimization to optimize the portfolio.
    """
    data = {stock: Ticker(stock).history(period="1y")['Close'] for stock in stocks}
    df = pd.DataFrame(data)

    # Calculate daily returns
    returns = df.pct_change().dropna()

    # Estimate covariance matrix using Ledoit-Wolf shrinkage method
    cov_matrix = LedoitWolf().fit(returns).covariance_

    # Mean returns
    mean_returns = returns.mean()

    # Portfolio optimization - Maximum Sharpe Ratio
    def portfolio_performance(weights):
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_std
        return portfolio_return, portfolio_std, sharpe_ratio

    # Initialize random portfolio weights
    num_stocks = len(stocks)
    weights = np.random.random(num_stocks)
    weights /= np.sum(weights)

    portfolio_return, portfolio_std, sharpe_ratio = portfolio_performance(weights)

    return {
        'return': portfolio_return,
        'risk': portfolio_std,
        'sharpe_ratio': sharpe_ratio,
    }
