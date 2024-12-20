# Django
from django.core.management.base import BaseCommand

# Models
from community.apps.rankings.models import RankingGroup


# Main Section
class Command(BaseCommand):
    help = "Create Ranking Group Post Hourly"

    def handle(self, *args, **kwargs):
        # RankingGroup.objects.create(model_type="POST", ranking_type="LIVE")
        pass
