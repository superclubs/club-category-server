from urllib.parse import urljoin

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from community.apps.badges.models import Badge


# Main Section
class Authentication(BaseAuthentication):
    def __init__(self):
        self.user_model = get_user_model()

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        partner_key = request.headers.get('Partner-Key')
        partner_secret_key = request.headers.get('Partner-Secret-Key')
        email = request.headers.get('CretaEmail')
        id_creta = request.headers.get('CretaID')

        if auth_header:
            return self.authenticate_with_token(auth_header)

        elif partner_key and partner_secret_key and email and id_creta:
            return self.authenticate_with_email_id_creta(email, id_creta, partner_key, partner_secret_key)

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

    def authenticate_with_email_id_creta(self, email, id_creta, partner_key, partner_secret_key):
        # 주어진 email과 id_creta로 사용자가 존재하는지 확인
        user = self.user_model.objects.filter(email=email, id_creta=id_creta).first()
        if user:
            return (user, None)

        # Superclub 서버에서 사용자 세부 정보를 가져옴
        user_data = self.fetch_user_data_from_superclub(None, partner_key, partner_secret_key, email, id_creta)
        if not user_data:
            raise AuthenticationFailed(_("Invalid user data from Superclub server"))

        # 사용자 정보를 생성
        user = self.get_or_create_user(user_data)
        return (user, None)

    def fetch_user_data_from_superclub(
        self,
        token=None,
        partner_key=None,
        partner_secret_key=None,
        email=None,
        id_creta=None
    ):
        url = urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/user/me")

        headers = {
            "Content-Type": "application/json"
        }
        if token:
            headers["Authorization"] = "Bearer " + str(token)
        if partner_key and partner_secret_key:
            headers["Partner-Key"] = partner_key
            headers["Partner-Secret-Key"] = partner_secret_key
        if email and id_creta:
            headers["CretaEmail"] = email
            headers["CretaID"] = id_creta

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

        # ID로 사용자가 이미 존재하는지 확인하고 업데이트 또는 생성
        id_user = filtered_user_data.get("id")
        id_creta = filtered_user_data.get("id_creta")

        user = self.user_model.objects.filter(id=id_user).first()
        users_removed = self.user_model.objects.filter(id_creta=id_creta).exclude(id=id_user)
        if users_removed.exists():
            users_removed.update(id_creta=None)

        if user:
            for key, value in filtered_user_data.items():
                try:
                    setattr(user, key, value)
                except Exception as e:
                    print(key)
                    print(value)

            user.save()
        else:
            user = self.user_model.objects.create(**filtered_user_data)

        if token:
            user.token_creta = token
            user.save()

        return user
