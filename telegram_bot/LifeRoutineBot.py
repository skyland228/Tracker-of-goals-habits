import os
from datetime import datetime
from dotenv import load_dotenv
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
load_dotenv()
bot = telebot.TeleBot(os.environ.get('get_info_token'))
habit_url = os.environ.get('API_HABITS_URL')
tgoal_url = os.environ.get('API_TGOALS_URL')
stats_url = os.environ.get('API_STATS_URL')
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
    payload = {
        "name": habit_name,
        "goal": selected_goal,
        }
    response = requests.post(habit_url, json=payload, params={"telegram_id": message.from_user.id})
    if response.status_code == 201:
      bot.send_message(
        message.chat.id,
        f"Создана привычка: {habit_name} → {selected_goal}")
    else:
      bot.send_message(
        message.chat.id,
        f"Ошибка создания: {response.text}")

@bot.message_handler(commands=['change_status_of_habit'])
def status_habit(message):
  habits = requests.get(habit_url,
                        params={"telegram_id": message.from_user.id},
                        ).json()
  habit_data = {}
  markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  for habit in habits:
    button_text = f"{habit['name']}" 
    status_icon = "✅" if habit["today_status"] else "❌"
    markup.add(KeyboardButton(f"{habit['name']} - {status_icon}"))
    habit_data[button_text] = (habit["id"])
  bot.send_message(message.chat.id, 'Выберите Привычку', reply_markup=markup)
  bot.register_next_step_handler(message,change_status, habit_data) # мы передали ид всех привычек
def change_status(message,habit_data):
  habit_name = message.text.split(' -')[0]
  habit_id = habit_data[habit_name]
  habit_status_url = f'http://127.0.0.1:8000/api/v1/habits/{habit_id}/toggle_status/'

  response = requests.post(habit_status_url, params={"telegram_id": message.from_user.id})
  if response.status_code == 200:
    bot.send_message(message.chat.id, f"Статус успешно изменён")
  else:
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['stats'])
def get_stats(message):
  response = requests.get(stats_url,params={'telegram_id': message.from_user.id})
  stat = response.json()
  streak = stat["streak"]
  completed = stat["total_progress"]["completed"]
  total = stat["total_progress"]["total"]
  percentage = stat["total_progress"]["percentage"]
  lines = []
  lines.append(f"Стрик: {streak}")
  lines.append(f"Прогресс: {completed} из {total}")
  lines.append(f"Процент выполнения: {percentage}%")
  text = "\n".join(lines)
  if response.status_code == 200:
    bot.send_message(message.chat.id,text)
  else:
    bot.send_message(message.chat.id, response)
   
bot.polling()