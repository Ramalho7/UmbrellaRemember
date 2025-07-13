import requests
import json
import os, sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CITY = 'Joao Pessoa'
STATE_CODE = 'Paraiba'
COUNTY_CODE = 'BR'
API_KEY = os.getenv('OPENWEATHER_API_KEY')
NTFY_CHANNEL = os.getenv('NTFY_CHANNEL')

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
        requests.post(
            NTFY_CHANNEL,
            data='Leve um guarda-chuva!',
            headers={'Title': 'Importante: Chuva HOJE!', 'Tags': 'warning, rain', 'Priority': '5'}
        )
    else:
        requests.post(
            NTFY_CHANNEL,
            data='Sem chuva para hoje!'
        )
    
if __name__ == '__main__':
    checkRainToday()
