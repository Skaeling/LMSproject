from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@email.com", username='user')
        self.course = Course.objects.create(title='TestCourse', description="тестовый курс")
        self.lesson = Lesson.objects.create(title='TestLesson', description='тестовый урок', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('lms:lesson_create')
        data = {
            "title": "DRF"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_create_video_url(self):
        url = reverse('lms:lesson_create')
        data = {
            "title": "DRF",
            "video_url": "vk.com"
        }
        response = self.client.post(url, data)
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            "title": "Django"
        }
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            result.get('title'), "Django"
        )

    def test_lesson_delete(self):
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lessons_list(self):
        url = reverse('lms:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': self.lesson.pk, 'video_url': None, 'title': 'TestLesson', 'description': 'тестовый урок',
                 'preview': None,
                 'course': self.course.pk, 'owner': self.user.pk}]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data, result)


class CourseTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com", username='test')
        self.course = Course.objects.create(title='TestCourse', description="тестовый курс", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        url = reverse('lms:course-list')
        data = {
            "title": "Python"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            "title": "Java"
        }
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            result.get('title'), "Java"
        )

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_courses_list(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()

        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.course.pk, 'title': 'TestCourse', 'preview': None, 'description': 'тестовый курс',
             'owner': self.user.pk}]}
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com", username='test')
        self.course = Course.objects.create(title='TestCourse', description="тестовый курс", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subs_change(self):
        url = reverse('lms:subs_create')
        data = {
            "id": self.course.pk
        }
        # Создаем подписку
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertTrue(Subscription.objects.all().exists())

        # Удаляем подписку
        response_2 = self.client.post(url, data)
        self.assertEqual(
            response_2.status_code, status.HTTP_200_OK
        )
        self.assertFalse(Subscription.objects.all().exists())
