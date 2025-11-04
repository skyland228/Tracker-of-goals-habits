from ..models import Habit

class GoalService:
    @staticmethod
    def depend_goal(temporal_goal, user):
        general_goal = temporal_goal.general_goal
        habits = Habit.objects.filter(
            goal__general_goal=general_goal,
            user = user,).select_related('goal')
        return general_goal, habits



