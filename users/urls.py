from django.urls import path

from users.views import UserUpdateAPIView, UserListAPIView, PaymentViewSet
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig

app_name = UsersConfig.name
router = SimpleRouter()
router.register('payments', PaymentViewSet)

urlpatterns = [
    path('profiles/', UserListAPIView.as_view(), name='users_list'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
] + router.urls

