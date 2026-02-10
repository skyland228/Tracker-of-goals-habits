import os
from dotenv import load_dotenv
import telebot
import requests
load_dotenv()
bot = telebot.TeleBot(os.environ.get('connect_token'))
API_BASE_URL = os.getenv("API_BASE_URL")
@bot.message_handler(commands=['start'])
def connect_user(message):
    parts = message.text.split()
    token = parts[1] if len(parts) > 1 else None 
    if not token:
        bot.send_message(message.chat.id, "Нет токена")
        return
    response = requests.post(
    API_BASE_URL,
    json={
        "token": token,
        "telegram_id": message.from_user.id
    })

    if response.status_code == 200:
        bot.send_message(message.chat.id, "Привязка успешна")
    else:
        bot.send_message(message.chat.id, "Ошибка привязки")

bot.polling()