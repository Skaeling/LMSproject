from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer, UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteAPIView(DestroyAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter ]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method')
    ordering_fileds = ('payment_date',)
    serializer_class = PaymentSerializer

