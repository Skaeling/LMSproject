from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Введите только цифры',
                                    verbose_name='Телефон')
    city = models.CharField(max_length=20, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars', blank=True,
                               null=True, help_text='Изображение размером не более 5 мб', verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    CARD = 'card'
    CASH = 'cash'

    PAYMENT_METHOD_CHOICES = [
        (CARD, 'оплата картой'),
        (CASH, 'оплата наличными'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    course_paid = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='paid_courses', blank=True,
                                    null=True)
    lesson_paid = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='paid_lessons', blank=True,
                                    null=True)
    payment_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user}, {self.payment_date}," \
            f"{self.course_paid if self.course_paid else ''}", \
            f"{self.lesson_paid if self.lesson_paid else ''}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
