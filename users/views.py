from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User, Payment
from .permissions import IsUser
from .serializers import PaymentSerializer, UserCreateSerializer, UserOwnerSerializer, \
    UserGuestSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserGuestSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserOwnerSerializer
        return UserGuestSerializer


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserOwnerSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)


class UserDeleteAPIView(DestroyAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method')
    ordering_fileds = ('payment_date',)
    serializer_class = PaymentSerializer
