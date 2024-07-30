# Django
from django.conf import settings
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

# Third party
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# DRF
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

description = _(
    """
클럽 카테고리 백엔드 서버 API 문서입니다.

# Response Data
<br/>
## 성공
```json
{
    "code": " ... ",
    "message": " ... ",
    "data": { ... }
}
```
<br/>
## 실패
```json
{
    "code": " ... ",
    "message": " ... ",
    "errors": { ... },
}
```
<br/>
## 세부 안내

`code` Status 코드입니다.

`message` 상세 메시지입니다.

`data` 응답 결과 데이터입니다.

`errors` 오류 발생시 나타나는 필드입니다.

<br/>"""
)

# Only expose to public in local and development.
public = bool(settings.DJANGO_ENV in ("local", "develop"))

# Fully exposed to only for local, else at least should be staff.
if settings.DJANGO_ENV == "local":
    permission_classes = (permissions.AllowAny,)
else:
    permission_classes = (permissions.AllowAny,)

schema_url_patterns = [
    path(r"^api/v1/", include("config.api_router")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

schema_view = get_schema_view(
    openapi.Info(
        title=_("커뮤니티 API 문서"),
        default_version="v1",
        description=description,
        contact=openapi.Contact(email="dev@runners.im"),
        license=openapi.License(name="Copyright 2022. Runners. all rights reserved."),
    ),
    public=public,
    permission_classes=permission_classes,
    patterns=schema_url_patterns,
)
