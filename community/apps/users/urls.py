# Django
from django.urls import path

# Views
from community.apps.users.api.views import UserAdminViewSet

app_name = 'users'
urlpatterns = [
    path('admin/user', UserAdminViewSet.as_view({'post': 'set_admin'})),
]
