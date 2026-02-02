from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'habits', views.HabitApiView)
urlpatterns = router.urls
