# Tracker of Goals & Habits

## Функциональность

Приложение поддерживает:

- создание глобальных целей;
- создание временных целей;
- связь временных целей с глобальной целью;
- создание привычек, привязанных к временным целям;
- отметку выполнения целей;
- отметку выполнения привычек по дням;
- расчёт прогресса по глобальной цели;
- расчёт пользовательской статистики по привычкам.

## Основные сущности

### GeneralGoal
Глобальная цель пользователя.

Поля:
- `name`
- `description`
- `user`
- `is_completed`
- `main_goal`
- `theme`

### TemporalGoal
Временная цель, связанная с глобальной целью.

Поля:
- `name`
- `description`
- `user`
- `deadline`
- `is_completed`
- `general_goal`

### Habit
Привычка, связанная с временной целью.

Поля:
- `name`
- `user`
- `created_at`
- `goal`

### HabitStatus
Статус выполнения привычки за конкретную дату.

Поля:
- `habit`
- `is_completed`
- `date`

### Theme
Тема оформления для целей.

Поля:
- `name`
- `color`
- `icon`

### User
Пользовательская модель на базе `AbstractUser`.

Дополнительные поля:
- `image`
- `bio`
- `telegram_id`

### TelegramLinkToken
Токен для привязки Telegram-аккаунта.

Поля:
- `user`
- `token`
- `used`
- `expires_at`

## Статистика

Для пользователя рассчитываются:

- текущий стрик;
- максимальный стрик;
- прогресс за сегодня;
- общий прогресс за всё время;
- процент выполненных статусов привычек.

## Технологии

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Django Templates
- HTML / CSS
- python-dotenv

## Установка и запуск

```bash
git clone https://github.com/skyland228/Tracker-of-goals-habits.git
cd Tracker-of-goals-habits/tracker

python -m venv venv
venv\Scripts\activate
# Linux / macOS:
# source venv/bin/activate

pip install django djangorestframework djangorestframework-simplejwt python-dotenv pillow

python manage.py migrate
python manage.py runserver