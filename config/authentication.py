from urllib.parse import urljoin

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from community.apps.badges.models import Badge


class Authentication(BaseAuthentication):
    def __init__(self):
        self.user_model = get_user_model()

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            return self.authenticate_with_token(auth_header)

        return None

    def authenticate_with_token(self, auth_header):
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        # 주어진 토큰으로 사용자가 존재하는지 확인
        user = self.user_model.objects.filter(token_creta=token).first()
        if user:
            return (user, token)

        # Superclub 서버에서 사용자 세부 정보를 가져옴
        user_data = self.fetch_user_data_from_superclub(token)
        if not user_data:
            raise AuthenticationFailed(_("Invalid user data from Superclub server"))

        # 사용자 정보를 업데이트하거나 생성
        user = self.get_or_create_user(user_data, token)
        return (user, token)

    def fetch_user_data_from_superclub(self, token):
        url = urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/user/me")

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(token)
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AuthenticationFailed(_("Failed to retrieve user data from Superclub server"))

        return response.json().get("data", None)

    def get_or_create_user(self, user_data, token=None):
        # User 모델에 존재하는 필드만 포함하도록 user_data 필터링
        user_fields = {field.name for field in self.user_model._meta.get_fields()}
        filtered_user_data = {k: v for k, v in user_data.items() if k in user_fields}

        # Badge 처리 (예시)
        badge_data = user_data.get("badge")
        if badge_data:
            filtered_user_data["badge"] = Badge.objects.filter(title_en=badge_data['title'],
                                                               model_type="COMMON").first()

        id_user = filtered_user_data.get("id")
        id_creta = filtered_user_data.get("id_creta")

        # 1. 기존 사용자 확인
        user = self.user_model.objects.filter(id=id_user).first()

        # 2. `id_creta`가 중복된 사용자 처리
        if id_creta:
            self.user_model.objects.filter(id_creta=id_creta).exclude(id=id_user).update(id_creta=None)

        # 3. 사용자 생성 또는 업데이트
        if user:
            # 기존 사용자 업데이트
            for key, value in filtered_user_data.items():
                setattr(user, key, value)
        else:
            # 새 사용자 생성
            user = self.user_model.objects.create(**filtered_user_data)

        # 4. 토큰 갱신
        if token:
            user.token_creta = token

        # 5. 저장
        user.save()

        return user
