from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lms/courses/preview', blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока')
    preview = models.ImageField(upload_to='lms/lessons/preview', blank=True, null=True, verbose_name="Превью")
    video_url = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='lessons',
                               verbose_name='Курс')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='is_subscribed', verbose_name='Подписчик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='is_subscribed',
                               verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
