from urllib.parse import urljoin

from django.conf import settings

from community.bases.modules.gateways import Gateway as BaseGateway


class Gateway(BaseGateway):
    def __init__(self):
        super().__init__(base_url=urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/"))

    def get_all_users(self):
        path = f"users/sync"
        return self.request(method="GET", path=path)

    def get_user_by_id(self, id: int, language: str):
        path = f"user/{id}"
        headers = {"Accept-Language": language}
        return self.request(method="GET", path=path, headers=headers)


gateway = Gateway()
