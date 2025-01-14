from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lms/courses/preview', blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=25, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока')
    preview = models.ImageField(upload_to='lms/lessons/preview', blank=True, null=True, verbose_name="Превью")
    video_url = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
