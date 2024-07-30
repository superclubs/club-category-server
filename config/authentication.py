# Python
from urllib.parse import urljoin

import requests
# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
# DRF
from rest_framework.exceptions import AuthenticationFailed

# Apps
from community.apps.badges.models import Badge


# Main section
class Authentication(BaseAuthentication):
    def __init__(self):
        self.user_model = get_user_model()

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        partner_key = request.headers.get('Partner-Key')
        partner_secret_key = request.headers.get('Partner-Secret-Key')

        if not auth_header:
            return None

        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        # 1. 주어진 토큰으로 사용자가 존재하는지 확인
        user = self.user_model.objects.filter(token_creta=token).first()
        if user:
            return (user, token)

        # 2. 사용자가 존재하지 않는 경우, Superclub 공통 서버에서 사용자 세부 정보를 가져옴
        url = urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/user/me")

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(token)
        }

        if partner_key and partner_secret_key:
            headers["Partner-Key"] = partner_key
            headers["Partner-Secret-Key"] = partner_secret_key

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AuthenticationFailed(_("Failed to retrieve user data from Superclub server"))

        data = response.json()
        user_data = data.get("data", None)
        if not user_data:
            raise AuthenticationFailed(_("Invalid user data from Superclub server"))

        # 3. 배지가 있으면 할당
        badge_data = user_data.pop("badge", None)
        user_data['token_creta'] = token

        # User 모델에 존재하는 필드만 포함하도록 user_data 필터링
        user_fields = {field.name for field in self.user_model._meta.get_fields()}
        filtered_user_data = {k: v for k, v in user_data.items() if k in user_fields}

        if badge_title_en := badge_data['title']:
            filtered_user_data["badge"] = Badge.objects.filter(title_en=badge_title_en, model_type="COMMON").first()

        # 4. ID로 사용자가 이미 존재하는지 확인하고 업데이트 또는 생성
        id_user = filtered_user_data["id"]
        id_creta = filtered_user_data["id_creta"]

        user = self.user_model.objects.filter(id=id_user).first()
        users_removed = self.user_model.objects.filter(id_creta=id_creta).exclude(id=id_user)
        if users_removed.exists():
            users_removed.update(id_creta=None)

        if user:
            for key, value in filtered_user_data.items():
                setattr(user, key, value)
            user.save()
        else:
            user = self.user_model.objects.create(**filtered_user_data)

        return (user, token)
