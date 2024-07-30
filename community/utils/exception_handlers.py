# Python
import logging
import traceback

# Django
from django.utils.translation import gettext_lazy as _

# Third Party
from drf_pretty_exception_handler import exception_handler
from rest_framework import exceptions, status

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
# DRF
from rest_framework import exceptions
from rest_framework.exceptions import *
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import set_rollback

# Apps
from community.utils.api.response import Response as CustomResponse

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {"PRETTY_STANDARD_PYTHON_EXCEPTIONS": True}
SETTINGS = {**DEFAULT_SETTINGS, **getattr(settings, "PRETTY_EXCEPTION_HANDLER", {})}
PRETTY_STANDARD_PYTHON_EXCEPTIONS = SETTINGS.get("PRETTY_STANDARD_PYTHON_EXCEPTIONS")

STATUS_CODE_MESSAGES = {
    status.HTTP_400_BAD_REQUEST: (400, _("값이 올바르지 않습니다.")),
    status.HTTP_401_UNAUTHORIZED: (401, _("접근 권한이 없습니다. 로그인 후 다시 시도해 주세요.")),
    status.HTTP_403_FORBIDDEN: (403, _("접근 권한이 없습니다.")),
    status.HTTP_404_NOT_FOUND: (404, _("데이터가 없습니다.")),
    status.HTTP_405_METHOD_NOT_ALLOWED: (405, _("허용되지 않은 메소드입니다.")),
    status.HTTP_406_NOT_ACCEPTABLE: (406, _("요청한 콘텐츠 형식을 제공할 수 없습니다.")),
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: (415, _("지원되지 않는 미디어 타입입니다.")),
    status.HTTP_429_TOO_MANY_REQUESTS: (429, _("요청이 너무 많습니다. 나중에 다시 시도해 주세요.")),
    status.HTTP_500_INTERNAL_SERVER_ERROR: (500, _("서버에 예기치 못한 오류가 발생했습니다.")),
}

DEFAULT_ERROR_MESSAGE = (500, _("서버에 예기치 못한 오류가 발생했습니다."))


def exception_handler(exc, context):
    logger.error(traceback.format_exc())

    if isinstance(exc, exceptions.APIException):
        data = {'status_code': exc.status_code, 'errors': {}}
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, list):
            data['errors']['non_field_errors'] = exc.detail
        elif isinstance(exc.detail, dict):
            data['errors'] = exc.detail
        else:
            data['errors']['non_field_errors'] = [exc.detail]

        set_rollback()
        response = Response(data, status=exc.status_code, headers=headers)
    else:
        response = None

    if response is None:
        if PRETTY_STANDARD_PYTHON_EXCEPTIONS:
            data = {'status_code': 500, 'errors': {}}
            data['errors']['non_field_errors'] = [f'{exc.__class__.__name__}: {exc}']
            return CustomResponse(status=500, code=500, message=DEFAULT_ERROR_MESSAGE[1], errors=data['errors'])
        return CustomResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, code=500, message=DEFAULT_ERROR_MESSAGE[1])

    data = response.data
    status_code = data.pop("status_code", response.status_code)

    # 각 예외 클래스에 대한 상태 코드 설정
    if isinstance(exc, ParseError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, AuthenticationFailed):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, NotAuthenticated):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, PermissionDenied):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, NotFound):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, MethodNotAllowed):
        status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    elif isinstance(exc, NotAcceptable):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
    elif isinstance(exc, UnsupportedMediaType):
        status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    elif isinstance(exc, Throttled):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS

    default_code, default_message = STATUS_CODE_MESSAGES.get(status_code, DEFAULT_ERROR_MESSAGE)

    if errors := data.pop("errors", None):
        stale_non_field_errors = errors.pop(api_settings.NON_FIELD_ERRORS_KEY, [])
        non_field_errors = []
        field_errors = errors

        for error_item in stale_non_field_errors:
            if isinstance(error_item, str):
                non_field_errors.append(error_item)
            else:
                field_errors.update(error_item)

        errors = {
            "field_errors": {k: list(map(str, v)) for k, v in field_errors.items()},
            "non_field_errors": non_field_errors,
        }

        print("field_errors : ", field_errors)
        print("non_field_errors : ", non_field_errors)

    return CustomResponse.from_drf_response(
        response,
        status=status_code,
        code=default_code,
        message=default_message,
        errors=errors
    )
