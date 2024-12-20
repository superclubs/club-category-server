from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from community.apps.badges.api.serializers import BadgeRetrieveSerializer
from community.apps.users.api.serializers import IconSwaggerSerializer
from community.apps.users.models import User
from community.bases.api.serializers import ModelSerializer


# Main Section
class UserSerializer(ModelSerializer):
    badge = BadgeRetrieveSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "profile_image_url",
            "card_profile_image_url",
            "banner_image_url",
            "badge_image_url",
            "username",
            "status",
            "badge",
        )


class UserWithIconsSerializer(UserSerializer):
    icons = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("icons",)

    @swagger_serializer_method(IconSwaggerSerializer(many=True))
    def get_icons(self, obj):
        if not hasattr(obj, "translate_icons_data"):
            return None
        return obj.translate_icons_data()


class UserMeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image_url",
            "card_profile_image_url",
            "badge_image_url",
            "username",
            "post_count",
            "comment_count",
            "status",
        )


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image_url",
            "card_profile_image_url",
            "badge_image_url",
            "username",
            "ring_color",
            "hash",
        )


class UsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )
