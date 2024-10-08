import numpy as np
import pandas as pd
from yfinance import Ticker
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def predict_stock_price(stock):
    """
    Predict stock price using Linear Regression.
    """
    ticker = Ticker(stock)
    df = ticker.history(period="1y")

    df['Return'] = df['Close'].pct_change().dropna()
    df['Future_Close'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    X = df[['Close', 'Volume', 'Return']]
    y = df['Future_Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model.predict(X_test[-1].values.reshape(1, -1))[0]  # Return the predicted next close price
