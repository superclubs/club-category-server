# DRF
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from community.bases.api.viewsets import GenericViewSet

# Models
from community.apps.reports.models import ReportGroup


# Main Section
class ReportGroupAdminViewSet(GenericViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = ReportGroup.available.all()
