import os
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import date, timedelta, datetime
import time
import dataframe_image as dfi
from pyrogram import Client


load_dotenv()

QUIVER_TOKEN = os.getenv('QUIVER_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


URL = 'https://api.quiverquant.com/beta/live/wallstreetbets'
HEADERS = {'Authorization': f'Token {QUIVER_TOKEN}'}


def send_message():
    with Client("my_account", api_id, api_hash) as app:
        app.send_photo(-1001545660559, photo=open('df_styled.png', 'rb'))


def today_stats():
    ts = datetime.now()
    ft = datetime(
        hour=8,
        year=int(format(ts, "%Y")),
        month=int(format(ts, "%m")),
        day=int(format(ts, "%d"))
    )
    today = format(ts, "%Y-%m-%d")

    todaydata = requests.get(
        'https://api.quiverquant.com/beta/historical/wallstreetbets',
        headers=HEADERS,
    )
    if ts > ft:
        data = todaydata.json()
        date_filter = [i for i in data if i['Date'] == today]
        ordered_data = sorted(date_filter, key=lambda d: d['Rank'])
        correct = pd.DataFrame(ordered_data[:20])
        correct.index = (correct.index + 1)
        correct_styled = correct.style.set_caption(f'<b> Топ-20 обсуждаемых компаний на REDDIT </b>').background_gradient().format({'Sentiment': "{:.2%}"})
        dfi.export(correct_styled, 'df_styled.png')
        send_message()
    else:
        pass


def main():

    while True:
        try:
            today_stats()
            time.sleep(60 * 60)

        except Exception as e:
            print(f"Бот упал с ошибкой: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
