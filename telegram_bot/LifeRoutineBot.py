import os
from dotenv import load_dotenv
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime


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
  today = datetime.now().date().isoformat()
  lines = []
  for habit in habits:
    name = habit["name"]
    goal = habit.get("goal", "")
    # Берем статусы
    statuses = habit.get('habit_statuses', [])
    today_status = None
    for status in statuses:
      if status['date'] == today:
          today_status = status
    if today_status is None:
        mark = "❌"  # сегодня не отмечал = не выполнено
    else:
        mark = "✅" if today_status['is_completed'] else "❌"
    if goal:
        lines.append(f"{name} — {mark}\n{goal}")
    else:
        lines.append(f"{name} — {mark}")
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

@bot.message_handler(commands=['add_habit'])
def start_add_habit(message):
    bot.send_message(message.chat.id, 'Введите название привычки')
    bot.register_next_step_handler(message, add_habit)

def add_habit(message):
    habit_name = message.text

    goals = requests.get(
        tgoal_url,
        params={"telegram_id": message.from_user.id},
    ).json()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for goal in goals:
        markup.add(KeyboardButton(goal["name"]))

    bot.send_message(
        message.chat.id,
        'Выберите цель',
        reply_markup=markup)
    bot.register_next_step_handler(message, finish, habit_name)

def finish(message, habit_name):
  selected_goal = message.text
  bot.send_message(
    message.chat.id,
    f"Создана привычка: {habit_name} → {selected_goal}")

bot.message_handler(commands=['status_habit'])
def status_habit(message):
   habits = requests.get(habit_url,
                         params={"telegram_id": message.from_user.id},
                         ).json()
   markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

bot.polling()