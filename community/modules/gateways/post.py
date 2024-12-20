from urllib.parse import urljoin

from django.conf import settings

from community.bases.modules.gateways import Gateway as BaseGateway


# Main Section
class Gateway(BaseGateway):
    def __init__(self):
        super().__init__(base_url=urljoin(settings.POST_SERVER_HOST, f"/api/{settings.POST_API_VERSION}/"))

    def sync_post(self, data):
        print("Sync Post")
        path = "post/sync"
        response = self.request(method="POST", path=path, json=data)
        print("response : ", response)
        return response

    def sync_like(self, data):
        print("Sync Like")
        path = "like/sync"
        response = self.request(method="POST", path=path, json=data)
        print("response : ", response)
        return response

    def sync_dislike(self, data):
        print("Sync Dislike")
        path = "dislike/sync"
        response = self.request(method="POST", path=path, json=data)
        print("response : ", response)
        return response

    def delete_post(self, data):
        print("Delete Post")
        path = "post"
        response = self.request(method="DELETE", path=path, json=data)
        print("response : ", response)
        return response


gateway = Gateway()
