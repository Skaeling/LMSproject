from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentStripeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['course_paid', 'payment_date', 'payment_amount',
                  'session_id', 'payment_link', 'status']


class UserOwnerSerializer(serializers.ModelSerializer):
    user_payments = PaymentStripeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'city', 'avatar', 'phone_number', 'user_payments', 'last_login']


class UserGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'city', 'avatar']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
