from django.shortcuts import get_object_or_404
from ..models import Habit, TemporalGoal, GeneralGoal


class GoalService:
    @staticmethod
    def depend_goal(temporal_goal, user):
        general_goal = temporal_goal.general_goal
        habits = Habit.objects.filter(
            goal__general_goal=general_goal,
            user = user,).select_related('goal')
        return general_goal, habits
    @staticmethod
    def toggle_goal_completion(goal):
        goal.is_completed = not goal.is_completed
        goal.save()
        return goal
    @staticmethod
    def progress_of_goal(goal):
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


