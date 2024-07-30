from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import HybridImageField as BaseHybridImageField


class HybridImageField(BaseHybridImageField):
    """
    Fixed version of HybridImageField of drf_extra_fields.

    Currently drf-yasg (1.20.0) generates wrong document for HybridImageField. this is
    temporary (or permanent) fix for it.

    Ref: https://github.com/Hipo/drf-extra-fields#drf-yasg-fix-for-base64-fields
    """

    class Meta:
        swagger_schema_fields = {
            "type": "string",
            "title": _("이미지 파일"),
            "description": _("이미지 파일 내용입니다. Base64 및 multipart/form-data를 지원합니다."),
            "read_only": False,
        }
