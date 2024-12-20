from community.bases.admin import CountAdmin


class CommunityVisitAdmin(CountAdmin):
    list_display = ("community", "profile")
    search_fields = ("community__title", "profile__user__email")

    fieldsets = (("정보", {"fields": ("community", "profile")}),)


class PostVisitAdmin(CountAdmin):
    list_display = ("post", "user")
    search_fields = ("post__title", "user__email")

    fieldsets = (("정보", {"fields": ("post", "user")}),)
