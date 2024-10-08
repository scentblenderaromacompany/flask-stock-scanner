from textblob import TextBlob
from bs4 import BeautifulSoup
import requests

def get_news_sentiment(stock_symbol):
    url = f"https://news.google.com/search?q={stock_symbol}%20stock"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = [a.text for a in soup.find_all('a')[:5]]
    sentiment = sum([TextBlob(article).sentiment.polarity for article in articles]) / len(articles)
    return sentiment
