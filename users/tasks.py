import datetime

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task(name="users.tasks.filter_users")
def filter_users():
    """Раз в 2 минуты фильтрует из БД пользователей с last_login более 30 дней и активным статусом.
    В случае их наличия запускает подзадачу по блокировке с задержкой в 10 секунд"""
    months_ago = timezone.now().today().date() - datetime.timedelta(days=30)
    users_to_block = User.objects.all().filter(last_login__lte=months_ago, is_active=True)
    if users_to_block.exists():
        block_users.apply_async(args=(list(users_to_block.values_list("id", flat=True)),), countdown=10)
        return "Users to block filtered"
    return "No users to block"


@shared_task(name="users.tasks.block_users")
def block_users(user_ids):
    """Проводит блокировку пользователя по полученным id путем смены статуса is_active на False"""
    users = User.objects.filter(id__in=user_ids)
    for u in users:
        u.is_active = False
        u.save()
    return "Inactive users blocked"
