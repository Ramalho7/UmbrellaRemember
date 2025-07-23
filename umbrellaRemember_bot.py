import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import asyncio

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CITY, STATE, COUNTRY = range(3)
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌂 Bem-vindo ao Umbrella Remember!"
    )
    await update.message.reply_text(
        """🌂 Comandos válidos:\n
        /checkRain
        """,
    )
    return CITY

async def checkRain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para começarmos, digite a sua cidade:")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text.strip()
    await update.message.reply_text("Agora digite o estado:")
    return STATE

async def get_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = update.message.text.strip()
    await update.message.reply_text("Agora digite o país (código, ex: BR):")
    return COUNTRY

async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['country'] = update.message.text.strip() 
    await checkRainRealTime(update, context)
    return ConversationHandler.END

async def checkRainRealTime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = context.user_data['city']
    state = context.user_data['state']
    country = context.user_data['country']
    
    geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={API_KEY}'
    response = requests.get(geo_url)
    if response.status_code != 200 or not response.json():
        await update.message.reply_text("Localização não encontrada ou erro na requisição.")
        return ConversationHandler.END

    geo_data = response.json()
    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']

    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt_br'
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        await update.message.reply_text("Erro ao buscar previsão do tempo.")
        return ConversationHandler.END

    forecast_data = forecast_response.json()
    today = forecast_data['list'][0]['dt_txt'][:10]
    rain_today = any(
        'rain' in item['weather'][0]['main'].lower() or 'chuva' in item['weather'][0]['main'].lower()
        for item in forecast_data['list'] if item['dt_txt'].startswith(today)
    )

    if rain_today:
        await update.message.reply_text("Vai chover hoje! Leve um guarda-chuva! ☂️")
    else:
        await update.message.reply_text("Dia de sol! ☀️")
        
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Consulta cancelada.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
        CommandHandler('start', start),
        CommandHandler('checkRain', checkRain)
        ],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_state)],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('checkRain', checkRain) # Preciso para que o comando envie a mensagem inicial e também sirva como entry point par ao bot
        ],
        
    )

    app.add_handler(conv_handler)
    app.run_polling()
