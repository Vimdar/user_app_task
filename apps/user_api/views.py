from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.user_api.constants import PAGINATE_USERS_BY
from apps.user_api.models import User
from apps.user_api.serializers import UserSerializer


USER_MODEL = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = PAGINATE_USERS_BY


class HealthcheckView(APIView):
    '''A healthcheck view'''
    def get(self, *args, **kwargs):
        _ = USER_MODEL.objects.count()
        return Response({'status': 'OK'})


class UserViewset(ModelViewSet):
    '''A viewset to CRUD Users'''
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.order_by('-updated_at')
    pagination_class = CustomPagination
