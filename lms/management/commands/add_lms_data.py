from django.core.management.base import BaseCommand
from django.core.management import call_command
from lms.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        call_command('loaddata', 'lms_fixture.json')
        self.stdout.write('Данные из фикстуры успешно загружены')
