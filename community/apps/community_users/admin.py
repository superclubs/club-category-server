# Models
from django.contrib import admin

# Apps
from community.apps.community_users.models import CommunityUser
from community.bases.admin import Admin


# Main Section
@admin.register(CommunityUser)
class CommunityUserAdmin(Admin):
    list_display = ("community", "user", "is_active")
