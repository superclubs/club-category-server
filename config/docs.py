# Django
from django.conf import settings
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _

# Third party
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# DRF
from rest_framework import permissions

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
public = bool(settings.ENVIRONMENT in ("local", "develop"))

# Fully exposed to only for local, else at least should be staff.
if settings.ENVIRONMENT == "local":
    permission_classes = (permissions.AllowAny,)
else:
    permission_classes = (permissions.AllowAny,)

schema_url_patterns = [
    path(r"^api/v1/", include("config.api_router")),
]

schema_view = get_schema_view(
    openapi.Info(
        title=_("포럼 커뮤니티 API 문서"),
        default_version="v1",
        description=description,
        contact=openapi.Contact(email="dev@runners.im"),
        license=openapi.License(name="Copyright 2022. Runners. all rights reserved."),
    ),
    public=public,
    permission_classes=permission_classes,
    patterns=schema_url_patterns,
)
