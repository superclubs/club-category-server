# Bases
from community.bases.admin import Admin


# Main Section
class CommentLikeAdmin(Admin):
    list_display = ("comment", "user")
    search_fields = ("comment__post", "user__email")

    fieldsets = (("정보", {"fields": ("comment", "user")}),)


class CommentDislikeAdmin(Admin):
    list_display = ("comment", "user")
    search_fields = ("comment__post", "user__email")

    fieldsets = (("정보", {"fields": ("comment", "user")}),)


class PostLikeAdmin(Admin):
    list_display = ("post", "user")
    search_fields = ("post__title", "user__email")

    fieldsets = (("정보", {"fields": ("post", "user")}),)


class PostDislikeAdmin(Admin):
    list_display = ("post", "user")
    search_fields = ("post__title", "user__email")

    fieldsets = (("정보", {"fields": ("post", "user")}),)
