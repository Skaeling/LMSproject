from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Payment
from .permissions import IsUser
from .serializers import PaymentSerializer, UserCreateSerializer, UserOwnerSerializer, \
    UserGuestSerializer, PaymentStripeSerializer
from .services import convert_rub_to_dollars, create_stripe_price, create_stripe_session, create_stripe_product, \
    change_stripe_session_status


class UserCreateAPIView(CreateAPIView):
    """Регистрирует профиль пользователя"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Представляет список всех пользователей"""
    serializer_class = UserGuestSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """Представляет детальный профиль пользователя в гостевом режиме или в полноценном(для владельца профиля)"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserOwnerSerializer
        return UserGuestSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Обновляет профиль текущего пользователя по переданному pk"""
    serializer_class = UserOwnerSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)


class UserDeleteAPIView(DestroyAPIView):
    """Удаляет профиль текущего пользователя по переданному pk"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method')
    ordering_fileds = ('payment_date',)
    serializer_class = PaymentSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Создает платеж, назначая создателя владельцем, возвращает пользователю ссылку на оплату"""
    serializer_class = PaymentStripeSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product = create_stripe_product(payment.course_paid.title, payment.course_paid.description)
        dollar_price = convert_rub_to_dollars(payment.payment_amount)
        final_price = create_stripe_price(dollar_price, stripe_product)
        session_id, payment_link = create_stripe_session(final_price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.status = change_stripe_session_status(payment.session_id)
        payment.save()


class PaymentRetrieveAPIView(RetrieveAPIView):
    """Представляет данные по платежу, согласно переданному pk.
    Обновляет в БД статус сессии на актуальный, если он не актуален"""
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentStripeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        session_id = instance.session_id

        current_status = instance.status
        new_status = change_stripe_session_status(session_id)

        if current_status != new_status:
            instance.status = new_status
            instance.save()
            print(f"Статус платежа №{instance.id} изменен на '{new_status}'")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
