import requests
import json
from datetime import date, timedelta
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ""

}
news_params = {
    "q": "tesla",
    "from": str(date.today()-timedelta(days=1)),
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize":10,
    "apiKey": ""
}

# parameters for smtplib
sender_email = "SENDER_EMAIL"
app_pwd = "app_pwd_SENDER"
receiver_email = "receiver_email"


## STEP 1: Use https://www.alphavantage.co/documentation/#daily get stock data
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_request = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_request.raise_for_status()
#print(stock_request.json())
with open("stockdata.json", "w") as file:
    json.dump(stock_request.json()["Time Series (Daily)"], file, indent=4)

with open("stockdata.json", "r") as file:
    stock_data = json.load(file)
new_stock_data = [float(stock_data[key]["4. close"]) for (key, value) in stock_data.items()]
delta = (new_stock_data[1] - new_stock_data[2]) / new_stock_data[2] * 100
if abs(delta) > 5:
    print("Big move")
    get_news = True
else:
    print("Small move")
    get_news = False

## STEP 2 get the news articles if movement in stock price is over 5%

if get_news:
    news_request = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_request.raise_for_status()
    print(news_request.json())
    with open("newsdata.json", "w") as file:
        json.dump(news_request.json()["articles"], file, indent=4)

    with open("newsdata.json", "r") as file:
        news_data = json.load(file)

    ## Prepare messages for sending

    to_send = [[item["title"], item["description"], item["url"]] for item in news_data[:3]]
    print(to_send)

    ## Send messages by email

    for item in to_send:
        if delta > 0:
            title = f"Tesla 🔺 {round(abs(delta), 2)} %"
        else:
            title = f"Tesla 🔻 {round(abs(delta), 2)} %"
        text = f"Subject:{title}\n\n{item[0]} \n{item[1]} \n\n{item[2]}"
        text = text.encode('utf-8')
        print(title)
        print(text)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=app_pwd)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=receiver_email,
                                msg=text)
else:
    print("Nothing to send")