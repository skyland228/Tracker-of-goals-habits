from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'users',views.UserApiView)

urlpatterns = router.urls
