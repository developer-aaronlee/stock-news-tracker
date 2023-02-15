import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
av_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "H8VXEK06NY75LDS4"
}

av_response = requests.get(url="https://www.alphavantage.co/query", params=av_parameters)
av_response.raise_for_status()
stock_data = av_response.json()
# print(stock_data)

# stock_daily = stock_data["Time Series (Daily)"]
# data_list = [y for x, y in stock_daily.items()]
# min_one_price = data_list[0]["4. close"]
# min_two_price = data_list[1]["4. close"]
# print(min_one_price, min_two_price)


def check_weekday(date):
    while date.weekday() > 4:
        date -= timedelta(1)
    return date


now = datetime.now()

yesterday_obj = now - timedelta(1)
check_yesterday = check_weekday(yesterday_obj)
yesterday = datetime.strftime(check_yesterday, "%Y-%m-%d")
# print(yesterday)

bef_yesterday_obj = check_yesterday - timedelta(1)
check_bef_yesterday = check_weekday(bef_yesterday_obj)
bef_yesterday = datetime.strftime(check_bef_yesterday, "%Y-%m-%d")
# print(bef_yesterday)


yesterday_price = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
bef_yesterday_price = float(stock_data["Time Series (Daily)"][bef_yesterday]["4. close"])
# print(yesterday_price, bef_yesterday_price)

volatility = round((((yesterday_price - bef_yesterday_price) / yesterday_price) * 100), 2)
# print(volatility)
title = ""
if volatility >= 0.03:
    title = f"TSLA: 🔺{volatility}%"
elif volatility <= -0.03:
    title = f"TSLA: 🔻{volatility * -1}%"
# print(title)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_parameters = {
    "qInTitle": COMPANY_NAME,
    "language": "en",
    "apiKey": "00ae90bcc97146fd92bb0da7d238c74b"
}

news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

top_news = news_data["articles"][:3]
# print(top_news)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
account_sid = "AC5fa6c5a6eb0469ffa205f93d360898f4"
auth_token = "75520705d8deb32b60567fdce92072e6"

client = Client(account_sid, auth_token)

# formatted_news = [f"{title}\nHeadline: {x['title']}\nBrief: {x['description']}" for x in top_news]
# print(formatted_news)

for x in top_news:
    # print(f"{title}\nHeadline: {x['title']}\nBrief: {x['description']}")
    message = client.messages.create(
            body=f"{title}\nHeadline: {x['title']}\nBrief: {x['description']}",
            from_="+18667022307",
            to="+16078787777"
        )
    print(message.status)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

