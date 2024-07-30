# Third Party
# Local
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.phonenumber import to_python


def validate_international_phonenumber(value):
    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(_("연락처를 정확히 입력해 주세요."), code="invalid_phone_number")
