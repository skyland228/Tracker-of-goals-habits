from django.shortcuts import get_object_or_404

from ..models import Habit, TemporalGoal


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



