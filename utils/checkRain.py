import requests
from sqlalchemy.orm import sessionmaker
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model import User, engine, City, State
from dotenv import load_dotenv
from datetime import datetime
from utils.send_email import send_email

load_dotenv()

DBSession = sessionmaker(bind=engine)

API_KEY = os.getenv('OPENWEATHER_API_KEY')

def checkRain():
    db_session = DBSession()
    users = db_session.query(User).all()
    
    if not users:
        raise ValueError("Nenhum usuário encontrado")
    
    for user in users:
        try:
            city = user.city.city_name
            state = user.city.state.state_name
            country = user.city.state.country.country_name  
            
            geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={API_KEY}'
            response = requests.get(geo_url)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = data[0].get('lat')
                    lon = data[0].get('lon')
                    print(f"Geolocalização de {city}: Latitude {lat}, Longitude {lon}")
                else:
                    print(f"Não foi possível encontrar geolocalização para {city}, {state}, {country}")
                    continue
            else:
                print(f"Erro ao consultar a API de geolocalização para {city}, {state}, {country}")
                continue
            
            today = datetime.now().date()
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt_br'
            forecast_response = requests.get(forecast_url)
            if forecast_response.status_code != 200:
                print(f'Erro na requisição de previsão: {forecast_response.status_code}')
                continue
            
            forecast_data = forecast_response.json()
            
            rain_today = False
            
            for forecast in forecast_data['list']:
                forecast_time = datetime.fromtimestamp(forecast['dt'])
                if forecast_time.date() == today:
                    weather = forecast['weather'][0]['main'].lower()
                    if 'rain' in weather or 'chuva' in weather:
                        rain_today = True
            
            if rain_today:
                html_body = f"""
                <div style="text-align:center; font-family:Roboto, sans-serif; padding:20px;">
                <img src="https://images.unsplash.com/photo-1428592953211-077101b2021b?q=80&w=1000&auto=format&fit=crop" alt="Guarda-chuva" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
                    <h1 style="color:blue;">☂️ Importante: Chuva HOJE!</h1>
                    <p style="font-size:18px;">Olá, {user.name}</p>
                    <p style="font-size:16px;">Há previsão de chuva para hoje em {city}. Não se esqueça de levar um guarda-chuva!</p>
                    <p style="font-size:14px; color:gray;">Atenciosamente,<br><strong>Umbrella Remember</strong></p>
                </div>
                """
                send_email(
                    subject='Dia de chuva!',
                    html_body=html_body,
                    recipient=user.email
                )
            else:
                html_body = f"""
                <div style="text-align:center; font-family:Roboto, sans-serif; padding:20px; background-color:#f9f9f9; border-radius:10px;">
                <img src="https://images.unsplash.com/photo-1464660439080-b79116909ce7?q=80&w=1502&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Dia ensolarado" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
                    <h1 style="color:green;">☀️ Sem previsão de chuva hoje!</h1>
                    <p style="font-size:18px;">Olá, {user.name}</p>
                    <p style="font-size:16px;">Hoje o dia estará limpo e ensolarado em {city}. Aproveite o dia ao máximo!</p>
                    <p style="font-size:14px; color:gray;">Atenciosamente,<br><strong>Umbrella Remember</strong></p>
                </div>
                """
                send_email(
                    subject='Dia de sol!',
                    html_body=html_body,
                    recipient=user.email
                )
        
        except Exception as e:
            print(f"Erro ao processar usuário {user.name}: {e}")

if __name__ == "__main__":
    checkRain()