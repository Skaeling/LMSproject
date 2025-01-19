from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter ]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method')
    ordering_fileds = ('payment_date',)
    serializer_class = PaymentSerializer

