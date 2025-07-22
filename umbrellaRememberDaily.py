import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import telegram
import asyncio

load_dotenv()

CITY = os.getenv('CITY')
STATE_CODE = os.getenv('STATE_CODE')
COUNTY_CODE = os.getenv('COUNTY_CODE')
API_KEY = os.getenv('OPENWEATHER_API_KEY')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def checkRainToday():
    geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={CITY},{STATE_CODE},{COUNTY_CODE}&appid={API_KEY}'
    response = requests.get(geo_url)
    if response.status_code != 200:
        print(f'Erro na requisição: {response.status_code}')
        return
    geo_data = response.json()
    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']

    today = datetime.now().date()

    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt_br'
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        print(f'Erro na requisição de previsão: {forecast_response.status_code}')
        return
    forecast_data = forecast_response.json()

    rain_today = False

    for forecast in forecast_data['list']:
        forecast_time = datetime.fromtimestamp(forecast['dt'])
        if forecast_time.date() == today:
            weather = forecast['weather'][0]['main'].lower()
            if 'rain' in weather or 'chuva' in weather:
                rain_today = True

    if rain_today:
        asyncio.run(send_telegram_message("Leve um guarda-chuva!"))
    else:
        asyncio.run(send_telegram_message("Dia de sol! ☀️"))

if __name__ == '__main__':
    checkRainToday()