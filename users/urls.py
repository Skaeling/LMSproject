from django.urls import path

from users.views import UserUpdateAPIView, UserListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('users_list/', UserListAPIView.as_view(), name='users_list'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
]

