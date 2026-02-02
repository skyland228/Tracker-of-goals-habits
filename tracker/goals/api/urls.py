from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'TG',views.TemporalGoalViewSet)
router.register(r'GG',views.GeneralGoalViewSet)
urlpatterns = router.urls