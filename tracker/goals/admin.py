from django.contrib import admin
from .models import TemporalGoal, GeneralGoal

@admin.register(TemporalGoal)
class TemporalGoalAdmin(admin.ModelAdmin):
  list_display = ('id','name','deadline','user', 'is_completed')
  list_display_links = ('name',)
  list_filter = ('user',)
  list_per_page = 5

@admin.register(GeneralGoal)
class GeneralGoalAdmin(admin.ModelAdmin):
  list_display = ('id','name','main_goal','user')
  list_display_links = ('name',)
  list_filter = ('user',)
  list_per_page = 5