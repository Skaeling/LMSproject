from django.urls import path

from lms.views import CourseViewSet, LessonUpdateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonCreateAPIView, LessonDestroyAPIView, SubscribeCreateAPIView
from rest_framework.routers import SimpleRouter
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('subs/create/', SubscribeCreateAPIView.as_view(), name='subs_create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
