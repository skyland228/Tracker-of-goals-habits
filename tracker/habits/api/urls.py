from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'habits', views.HabitApiView,basename='Habit')
router.register(r'habit-statuses', views.HabitStatusApiView)
urlpatterns = router.urls
