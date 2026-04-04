from django.shortcuts import get_object_or_404
from habits.models import Habit


class GoalService:
    """
    Сервисный слой для работы с целями.

    Содержит бизнес-логику, связанную с прогрессом целей,
    переключением статуса выполнения и получением связанных привычек.
    """
    @staticmethod
    def depend_goal(temporal_goal, user):
        """
        Возвращает глобальную цель временной цели и связанные с ней привычки пользователя.

        Метод получает родительскую глобальную цель для переданной временной цели
        и выбирает все привычки пользователя, которые относятся к этой глобальной цели.
        Используется для отображения связанных привычек на странице временной цели.
        """
        general_goal = temporal_goal.general_goal
        habits = Habit.objects.filter(
            goal__general_goal=general_goal,
            user = user,).select_related('goal')
        return general_goal, habits
    @staticmethod
    def toggle_goal_completion(goal):
        """
        Переключает статус выполнения цели.

        Меняет значение поля `is_completed` на противоположное,
        сохраняет объект и возвращает обновлённую цель.
        """
        goal.is_completed = not goal.is_completed
        goal.save()
        return goal
    @staticmethod
    def progress_of_goal(goal):
        """
        Рассчитывает процент выполнения глобальной цели.

        Прогресс определяется по доле выполненных временных целей.
        Если у глобальной цели указана главная подцель и она выполнена,
        к базовому прогрессу добавляется бонус 20%.
        Итоговое значение не может превышать 100.
        """
        total = goal.temporal_goal.count()
        if total == 0:
            return 0
        completed_goals = goal.completed_goals().count()
        base_progress = int((completed_goals / total) * 100)
        if goal.main_goal and goal.main_goal.is_completed:
            main_goal_bonus = 20
            return min(100, base_progress + main_goal_bonus) # костыль, чтобы не выйти за 100
            # в дальнейшем придумаю как более грамотно в 100 укладывать все
        return base_progress


