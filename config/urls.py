from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from config.docs import schema_view
from config.redirects import redirect_swagger_view

admin.site.site_header = "FORUM CATEGORY"
admin.site.site_title = "FORUM CATEGORY"
admin.site.index_title = "포럼 카테고리 관리자 페이지"

urlpatterns = (
    [
        path("", redirect_swagger_view),
        # Admin
        path("jet/", include("jet.urls", "jet")),
        path(settings.ADMIN_URL, admin.site.urls),
        # Allauth
        path("accounts/", include("allauth.urls")),
        # Advanced Filters
        path("advanced_filters/", include("advanced_filters.urls")),
        # django-health-check
        path("ht/", include("health_check.urls")),
        # summernote
        path("summernote/", include("django_summernote.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# API URLS
urlpatterns += [
    # API base url
    path("api/", redirect_swagger_view),
    path("api/v1/", include("config.api_router")),
    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
