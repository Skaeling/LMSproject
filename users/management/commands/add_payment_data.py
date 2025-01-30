from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()

        call_command('loaddata', 'payment_fixture.json')
        self.stdout.write('Данные из фикстуры успешно загружены')
