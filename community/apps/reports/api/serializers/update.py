# Django Rest Framework
from rest_framework.exceptions import ParseError

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.reports.models import ReportChoice


# Main Section
class ReportChoiceUpdateSerializer(ModelSerializer):
    class Meta:
        model = ReportChoice
        fields = ('title', 'content', 'is_active')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        title = validated_data.get('title', None)
        content = validated_data.get('content', None)

        if instance.is_default:
            if title or content:
                raise ParseError('기본 신고 사유는 수정할 수 없습니다.')
        instance.update(**validated_data)
        return instance
