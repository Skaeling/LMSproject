from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Course


@shared_task(name='lms.tasks.send_notification')
def send_notification(pk):
    course = Course.objects.get(pk=pk)
    emails = list(course.is_subscribed.all().values_list('user__email', flat=True))
    send_mail(
        subject='Ваш курс обновлён',
        message='В курсе, на который вы подписаны, появились новые уроки',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails
    )
