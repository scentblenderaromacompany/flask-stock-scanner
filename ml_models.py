import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import yfinance as yf

def predict_price(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period='1y')
    hist['Days'] = np.arange(len(hist))
    
    X = hist[['Days']]
    y = hist['Close']
    
    model = LinearRegression()
    model.fit(X, y)

    next_day = len(hist)
    predicted_price = model.predict([[next_day]])
    return predicted_price[0]
