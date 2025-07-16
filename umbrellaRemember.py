import requests
import json
import os, sys
from datetime import datetime
from dotenv import load_dotenv
import ezgmail

ezgmail.init()
load_dotenv()

CITY = os.getenv('CITY')
STATE_CODE = os.getenv('STATE_CODE')
COUNTY_CODE = os.getenv('COUNTY_CODE')
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
                
    recipients = os.getenv('RECIPIENTS').split(',')
    recipients = [email.strip() for email in recipients]
    
    if rain_today:
        html_body = """
        <div style="text-align:center; font-family:Roboto, sans-serif; padding:20px;">
        <img src="https://images.unsplash.com/photo-1428592953211-077101b2021b?q=80&w=1000&auto=format&fit=crop" alt="Guarda-chuva" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
            <h1 style="color:blue;">☂️ Importante: Chuva HOJE!</h1>
            <p style="font-size:18px;">Olá,</p>
            <p style="font-size:16px;">Há previsão de chuva para hoje. Não se esqueça de levar um guarda-chuva!</p>
            <p style="font-size:14px; color:gray;">Atenciosamente,<br><strong>Umbrella Remember</strong></p>
        </div>
        """
        for recipient in recipients:
            ezgmail.send(recipient, 'Leve um guarda-chuva!', html_body, mimeSubtype='html')
        requests.post(
            NTFY_CHANNEL,
            data='Leve um guarda-chuva!',
            headers={'Title': 'Importante: Chuva HOJE!', 'Tags': 'warning, rain', 'Priority': '5'}
        )
    else:
        html_body = """
        <div style="text-align:center; font-family:Roboto, sans-serif; padding:20px; background-color:#f9f9f9; border-radius:10px;">
        <img src="https://images.unsplash.com/photo-1464660439080-b79116909ce7?q=80&w=1502&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Dia ensolarado" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
            <h1 style="color:green;">☀️ Sem previsão de chuva hoje!</h1>
            <p style="font-size:18px;">Olá,</p>
            <p style="font-size:16px;">Hoje o dia estará limpo e ensolarado. Aproveite o dia ao máximo!</p>
            <p style="font-size:14px; color:gray;">Atenciosamente,<br><strong>Umbrella Remember</strong></p>
        </div>
        """
        for recipient in recipients:
            ezgmail.send(recipient, 'Dia de sol!', html_body, mimeSubtype='html')
        requests.post(
            NTFY_CHANNEL,
            data='Sem chuva para hoje!'
        )
    
if __name__ == '__main__':
    checkRainToday()
