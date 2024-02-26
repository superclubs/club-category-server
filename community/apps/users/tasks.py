# Django
from celery import shared_task

# Serializer
from community.apps.users.api.serializers import UserProfileSerializer

# Model
from community.apps.users.models import User


# Main Section
@shared_task(name='user_task', bind=True)
def user_task(self, user_id, username, email, phone, level, grade_title, ring_color, badge_image_url,
              profile_image_url, banner_image_url, friend_count, status, wallet_address):
    print('========== User: user_task ==========')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    user.username = username
    user.email = email
    user.phone = phone
    user.level = level
    user.grade_title = grade_title
    user.ring_color = ring_color
    user.badge_image_url = badge_image_url
    user.profile_image_url = profile_image_url
    user.banner_image_url = banner_image_url
    user.friend_count = friend_count
    user.status = status
    user.wallet_address = wallet_address

    user.save()


@shared_task(name='sync_user_task', bind=True)
def sync_user_task(self, user_id):
    print('========== User: sync_user_task ==========')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    user_data = UserProfileSerializer(instance=user).data

    user.profiles.update(user_data=user_data)
    user.communities.update(user_data=user_data)
    user.posts.filter(is_temporary=False, is_active=True, is_deleted=False).update(user_data=user_data)
