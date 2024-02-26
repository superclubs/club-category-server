# Django Rest Framework
from rest_framework import serializers

# Serializers
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.post_tags.models.index import PostTag


# Main Section
class PostTagListSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='tag', queryset=PostTag.available.all())

    class Meta:
        model = PostTag
        fields = ('id', 'title')
