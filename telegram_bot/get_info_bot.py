import os
from dotenv import load_dotenv
import telebot
import requests

load_dotenv()
bot = telebot.TeleBot(os.environ.get('get_info_token'))
habit_url = os.environ.get('API_HABITS_URL')
tgoal_url = os.environ.get('API_TGOALS_URL')

@bot.message_handler(commands=['get_habits'])
def get_habits(message):
  params = {
    "telegram_id": message.from_user.id}
  response = requests.get(habit_url, params=params)
  if response.status_code != 200:
    bot.send_message(message.chat.id, 'Ошибка API')
    return
  habits = response.json()
  if not habits:
    bot.send_message(message.chat.id, 'Привычек нет')
    return
  lines = []
  for habit in habits:
      name = habit["name"]
      goal = habit["goal"]
      if goal:
          lines.append(f"{name} → {goal}")
      else:
          lines.append(name)

  text = "\n".join(lines)
  bot.send_message(message.chat.id, text)

bot.message_handler(commands = ['get_tgoals'])
def get_tgoals(message):
  params = {
  "telegram_id": message.from_user.id}
  response = requests.get(tgoal_url, params=params)
  if response.status_code != 200:
    bot.send_message(message.chat.id, "Ошибка API")
    return
  tgoals = response.json()
  if not tgoals:
    bot.send_message(message.chat.id, "Не найдено подцелей")
  lines = []
  for tgoal in tgoals:
    lines.append(tgoal['name'])
    lines.append(tgoal['deadline'])
    lines.append(tgoal['is_completed'])
    lines.append(tgoal['goal'])
  text = "\n".join(lines)
  bot.send_message(message.chat.id, text)

bot.polling()