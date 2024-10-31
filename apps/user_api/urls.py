from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.user_api.views import UserViewset, HealthcheckView


urlpatterns = [
    path('healthcheck/', HealthcheckView.as_view(), name='healthcheck'),
]
router = SimpleRouter()
router.register(r'user', UserViewset, basename='user')
