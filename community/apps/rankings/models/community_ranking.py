# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Bases
from community.bases.models import Model

# Manager
from community.apps.rankings.models.manager.index import RankingManager

# Models
from community.apps.communities.models import Community
from community.apps.badges.models import Badge


# Main Section
class ClubRankingManager(RankingManager):
    def create_rankings(self, prev_ranking_group, new_ranking_group):

        # 1. Get all communities
        communities = Community.available.all()
        community_count = communities.count()

        # 2. Get prev_rankings
        prev_rankings = None
        if prev_ranking_group:
            prev_rankings = prev_ranking_group.community_rankings

        # 3. Set ranking_list from communities and prev_rankings
        ranking_list = []
        for index, community in enumerate(communities):

            # Default rank, point when no prev_ranking
            old_rank = community_count
            old_point = 0
            old_point_rank = 0

            if prev_rankings:
                if ranking_old := prev_rankings.filter(community=community, is_active=True, is_deleted=False).first():
                    old_rank = ranking_old.rank
                    old_point = ranking_old.point
                    old_point_rank = ranking_old.point_rank

            ranking_new = CommunityRanking(
                ranking_group=new_ranking_group,
                prev_ranking_group=prev_ranking_group,
                community=community,
                point=community.point,
                point_change=community.point - old_point,  # Set point_change
                old_rank=old_rank,
                old_point_rank=old_point_rank,
                level=community.level
            )
            ranking_list.append(ranking_new)

        # 4. Set rank, rank_change from point
        ranking_list = sorted(ranking_list, key=lambda x: x.point, reverse=True)  # Sort by rank_change
        for index, ranking in enumerate(ranking_list):
            ranking.point_rank = index + 1
            ranking.point_rank_change = ranking.old_point_rank - ranking.point_rank

        # 5. Set rank, rank_change from point_change
        if new_ranking_group.ranking_type in ['LIVE', 'WEEKLY', 'MONTHLY']:
            ranking_list = sorted(ranking_list, key=lambda x: x.point_change,
                                  reverse=True)  # 포인트 변경 순으로 리스트 순서 재배치

        elif new_ranking_group.ranking_type == 'RISING':
            ranking_list = sorted(ranking_list, key=lambda x: x.point_rank_change,
                                  reverse=True)  # 포인트 순위 변경 순으로 리스트 순서 재배치

        for index, ranking in enumerate(ranking_list):
            ranking.rank = index + 1
            ranking.rank_change = ranking.old_rank - ranking.rank

        # TODO: 리팩토링
        live_badge = Badge.available.get(title='Live Best', model_type='CLUB')
        weekly_badge = Badge.available.get(title='Weekly Best', model_type='CLUB')
        monthly_badge = Badge.available.get(title='Monthly Best', model_type='CLUB')
        rising_badge = Badge.available.get(title='Rising Club', model_type='CLUB')

        # 6. Update community ranking
        for index, ranking in enumerate(ranking_list):

            if new_ranking_group.ranking_type == 'LIVE':
                ranking.community.live_rank = ranking.rank
                ranking.community.live_rank_change = ranking.rank_change

                if ranking.community.live_rank < 11 and not ranking.community.badges.filter(id=live_badge.id, is_active=True, is_deleted=False):
                    ranking.community.badges.add(live_badge.id)
                if ranking.community.live_rank > 10 and ranking.community.badges.filter(id=live_badge.id, is_active=True, is_deleted=False):
                    ranking.community.badges.remove(live_badge)

            elif new_ranking_group.ranking_type == 'WEEKLY':
                ranking.community.weekly_rank = ranking.rank
                ranking.community.weekly_rank_change = ranking.rank_change

                if ranking.community.weekly_rank < 11 and not ranking.community.badges.filter(id=weekly_badge.id, is_active=True, is_deleted=False):
                    ranking.community.badges.add(weekly_badge.id)
                if ranking.community.weekly_rank > 10 and ranking.community.badges.filter(id=weekly_badge.id, is_active=True, is_deleted=False):
                    ranking.community.badges.remove(weekly_badge)

            elif new_ranking_group.ranking_type == 'MONTHLY':
                ranking.community.monthly_rank = ranking.rank
                ranking.community.monthly_rank_change = ranking.rank_change

                if ranking.community.monthly_rank < 11 and not ranking.community.badges.filter(id=monthly_badge.id):
                    ranking.community.badges.add(monthly_badge.id)
                if ranking.community.monthly_rank > 10 and ranking.community.badges.filter(id=monthly_badge.id):
                    ranking.community.badges.remove(monthly_badge)

            elif new_ranking_group.ranking_type == 'RISING':
                ranking.community.rising_rank = ranking.rank
                ranking.community.rising_rank_change = ranking.rank_change

                if ranking.community.rising_rank < 11 and not ranking.community.badges.filter(id=rising_badge.id):
                    ranking.community.badges.add(rising_badge.id)
                if ranking.community.rising_rank > 10 and ranking.community.badges.filter(id=rising_badge.id):
                    ranking.community.badges.remove(rising_badge)

            ranking.community.save()

        community_rankings = CommunityRanking.objects.bulk_create(ranking_list)
        return community_rankings


class CommunityRanking(Model):
    # FK
    ranking_group = models.ForeignKey('rankings.RankingGroup', verbose_name=_('Ranking Group'), on_delete=models.CASCADE,
                                      related_name='community_rankings')
    prev_ranking_group = models.ForeignKey('rankings.RankingGroup', verbose_name=_('Prev Ranking Group'),
                                           on_delete=models.SET_NULL, null=True, blank=True)
    community = models.ForeignKey('communities.Community', verbose_name=_('Community'), on_delete=models.CASCADE,
                                  related_name='community_rankings')

    # Rank
    rank = models.IntegerField(_('Rank'), default=0)
    old_rank = models.IntegerField(_('Old Rank'), default=0)
    rank_change = models.IntegerField(_('Rank Change'), default=0)

    point_rank = models.IntegerField(_('Point Rank'), default=0)
    old_point_rank = models.IntegerField(_('Old Point Rank'), default=0)
    point_rank_change = models.IntegerField(_('Point Rank Change'), default=0)

    point_change = models.IntegerField(_('Point Change'), default=0)
    point = models.IntegerField(_('Point'), default=0)

    level = models.IntegerField(_('Level'), default=1)

    objects = ClubRankingManager()

    class Meta:
        verbose_name = verbose_name_plural = _('Community Ranking')
        ordering = ['-created']
