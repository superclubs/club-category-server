# config/middleware.py
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.GET.get("token")
        if token:
            user = self.authenticate_with_token(token)
            if user is not None:
                if user.is_staff or user.is_superuser:
                    self.login_with_backend(request, user)
                else:
                    return None
        return None

    def authenticate_with_token(self, token):
        try:
            user = User.objects.get(token_creta=token)
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 명시적으로 backend 설정
            return user
        except User.DoesNotExist:
            user = self.fetch_user_from_superclub(token)
            if user:
                user.token_creta = token
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
                return user
            raise AuthenticationFailed("User does not exist")

    def fetch_user_from_superclub(self, token):
        url = urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/user/me")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(token)
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AuthenticationFailed("Failed to retrieve user data from Superclub server")

        data = response.json()
        user_data = data.get("data", None)
        if not user_data:
            raise AuthenticationFailed("Invalid user data from Superclub server")

        # User ID 확인
        id = user_data.get("id")
        id_creta = user_data.get("id_creta")
        if not (id and id_creta):
            raise AuthenticationFailed("User ID is missing from Superclub data")

        try:
            # 로컬 데이터베이스에서 유저 검색
            user = User.objects.get(id_creta=id_creta)
            return user
        except User.DoesNotExist:
            # 로컬에 유저가 없는 경우 에러 반환
            raise AuthenticationFailed("User exists on Superclub but not locally.")

    def login_with_backend(self, request, user):
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # 명시적으로 backend 설정
        login(request, user)
