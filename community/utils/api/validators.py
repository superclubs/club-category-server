from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


def image_non_empty(value):
    if not value:
        raise serializers.ValidationError(_("빈 이미지는 허용되지 않습니다."))

    return value
