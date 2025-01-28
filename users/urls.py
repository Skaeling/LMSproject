from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserUpdateAPIView, UserListAPIView, PaymentViewSet, UserCreateAPIView, UserDeleteAPIView, \
    UserRetrieveAPIView
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig

app_name = UsersConfig.name
router = SimpleRouter()
router.register('payments', PaymentViewSet)

urlpatterns = [
                  path('profiles/', UserListAPIView.as_view(), name='users_list'),
                  path('profiles/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
                  path('profiles/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
                  path('register/', UserCreateAPIView.as_view(), name='register'),
                  path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
                  path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
                  path('profile/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user_delete'),
              ] + router.urls
