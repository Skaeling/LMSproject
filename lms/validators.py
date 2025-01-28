from rest_framework.serializers import ValidationError


def validate_video_url(value):
    if 'youtube.com' not in value.lower():
        raise ValidationError("Урок может быть размещен только на ресурсе: 'youtube.com'")