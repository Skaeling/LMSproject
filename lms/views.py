import datetime

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from lms.paginators import LMSPaginator
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer

from lms.models import Course, Lesson, Subscription
from lms.tasks import send_notification
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = LMSPaginator

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
            # self.permission_classes = (AllowAny,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        """При условии отсутствия обновления курса в прошедшие 4 часа отправляет подписчикам электронное уведомление"""

        last_updated = serializer.instance.updated_at
        course = serializer.save()
        time_difference = course.updated_at - last_updated
        if course.is_subscribed.exists() and time_difference > datetime.timedelta(hours=4):
            send_notification.delay(course.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    """Создает урок, назначая создателя владельцем урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Представляет список уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LMSPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представляет урок по переданному pk"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновляет урок по переданному pk"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаляет урок по указанному pk"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)


class SubscribeCreateAPIView(generics.CreateAPIView):
    """Обновляет статус подписки на противоположный текущему"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('id')
        course_item = get_object_or_404(Course.objects.all(), pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = f'Подписка на курс {course_item.title} удалена'
        else:
            subs_item.create(user=user, course=course_item)
            message = f'Подписка на курс {course_item.title} добавлена'
        return Response({"message": message})
