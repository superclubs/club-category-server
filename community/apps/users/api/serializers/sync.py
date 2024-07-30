from rest_framework import serializers

from community.apps.badges.models import Badge
from community.apps.users.models import User
from community.apps.users.tasks import sync_user_data_task
from community.bases.api.serializers import ModelSerializer


# Main Section
class AdminUserSyncSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("id", "password", "username")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.setdefault("is_staff", True)
        validated_data.setdefault("is_superuser", True)
        instance = User.objects.create(**validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.setdefault("is_staff", True)
        validated_data.setdefault("is_superuser", True)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserSyncSerializer(ModelSerializer):
    id = serializers.IntegerField()
    badge_title_en = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            # Main
            "id",
            "username",
            "email",
            "phone",
            "gender",
            "birth",
            "nation",
            "religion",
            "level",
            "grade_title",
            "ring_color",
            "status",
            "wallet_address",
            "badge_title_en",
            # Image
            "badge_image_url",
            "profile_image_url",
            "card_profile_image_url",
            "banner_image_url",
            # Count
            "friend_count",
        )

    def update(self, instance, validated_data):
        if badge_title_en := validated_data.pop("badge_title_en", None):
            validated_data["badge"] = Badge.available.filter(title_en=badge_title_en, model_type="COMMON").first()
        instance.update(**validated_data)

        # Sync user_data
        sync_user_data_task.delay(instance.id)

        return instance
