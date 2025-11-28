from django.utils import timezone
from habits.models import Habit, HabitStatus


class HabitServices:
  @staticmethod
  def ensure_habit_statuses_exist(user):
      habits = Habit.objects.filter(user = user) # просто получаем все привычки пользователя
      date = timezone.date()
      all_existing_statuses = HabitStatus.object.filter(habit__user = user).values('habit_id','date') # получаем статусы только с привычкой и датой, данные
      existing_dates_by_habit = {}
      for status in all_existing_statuses:
        habit_id = status['habit_id']
        date = status['date']
        if habit_id not in existing_dates_by_habit:
          existing_dates_by_habit[habit_id] = set() # если нет для этой привычки ключ с мн-вом дат то я создаю
        existing_dates_by_habit[habit_id].add(date) # добавляем нашу дату статуса в место привычки  
      statuses_to_create = [] # список чтобы потом все создать за один раз
      for habit in habits:
        existing_dates = existing_dates_by_habit.get(habit.id, set()) # получаем мн-во дат для привычки, которая из цикла в данный момент
        start_date = habit.created_at
        current_date = start_date
        end_date = timezone.date()
        while current_date <= end_date:
          if current_date not in existing_dates:
            statuses_to_create.append(HabitStatus(habit = habit, date = current_date, is_completed = False))
      if statuses_to_create:
        HabitStatus.objects.bulk_create(statuses_to_create, batch_size=100)
         

         