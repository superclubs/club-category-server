# DRF
from rest_framework.permissions import BasePermission


# Main Section
class PostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.community:
            if view.action in ["post_report", "post_comment", "post_emoji", "post_unemoji"]:
                if request.user.id is None:
                    return False

        return True
