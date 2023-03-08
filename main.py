import requests
from twilio.rest import Client
from config import *

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


# get news from news api searching for 3 recent articles
# on Tesla Inc
def get_news(up_or_down, change):
    # params and url for api request
    params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": API_KEY_N,

    }
    url = "https://newsapi.org/v2/everything?"
    # make the call to api
    # get all the articles from the data
    # then take the first 3 articles
    response = requests.get(url, params=params)
    response.raise_for_status()
    news = response.json()["articles"]
    articles = news[:3]
    # using list comprehension format it to be sent out as a text
    formatted_articles = [
        f"{STOCK}:{up_or_down}{change}% Healine: {article['title']}. \nBrief: {article['description']}" for article in
        articles]
    # send formatted articles as texts
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=FROM_NUM,
            to=TO_NUM

        )
        print(article)


def get_stock_change():
    # using alphavantage get stock prices from yesterday and the day before
    # to find the amount it has changed
    stock_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "outputsize": "compact",
        "apikey": API_KEY_S
    }
    url = "https://www.alphavantage.co/query?"
    response = requests.get(url, params=stock_params)
    response.raise_for_status()
    # accessing the json returned from the api
    # isolating the closing prices
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = float(yesterday_data["4. close"])
    day_before_yesterday_data = data_list[1]
    day_before_yesterday_price = float(day_before_yesterday_data["4. close"])
    up_or_down = None
    # calc the percent change
    diff = yesterday_closing_price - day_before_yesterday_price
    if diff > 0:
        up_or_down = " 🔺"
    else:
        up_or_down = "🔻"
    change = abs(round((diff / yesterday_closing_price) * 100, 2))

    # if the stock has changed more than 5%
    if change > 5:
        get_news(up_or_down, change)


# starts the program
get_stock_change()
