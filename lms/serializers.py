from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(required=False, allow_blank=True, validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = '__all__'

    def validate(self, data):
        if 'video_url' in data and not data['video_url']:
            # Удаляем поле video_url до валидации, если оно не содержит данных
            data.pop('video_url')
        return data


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if obj.is_subscribed.filter(user=user):
            return True
        return False

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'lessons_count', 'lessons', 'owner', 'is_subscribed', )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
