# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from community.apps.badges.models import Badge
from community.apps.posts.models import Post

# Bases
from community.bases.models import Model

# Manager
from community.apps.rankings.models.manager.index import RankingManager


# Main Section
class PostRankingManager(RankingManager):
    def create_rankings(self, prev_ranking_group, new_ranking_group):

        # 1. Get all posts
        posts = Post.available.filter(is_temporary=False, is_default=False, is_agenda=False)
        post_count = posts.count()

        # 2. Get prev_rankings
        prev_rankings = None
        if prev_ranking_group:
            prev_rankings = prev_ranking_group.post_rankings

        # 3. Set ranking_list from posts and prev_rankings
        ranking_list = []
        for index, post in enumerate(posts):

            # Default rank, point when no prev_ranking
            old_rank = post_count
            old_point = 0
            old_point_rank = 0

            if prev_rankings:
                if ranking_old := prev_rankings.filter(post=post, is_active=True, is_deleted=False).first():
                    old_rank = ranking_old.rank
                    old_point = ranking_old.point
                    old_point_rank = ranking_old.point_rank

            ranking_new = PostRanking(
                ranking_group=new_ranking_group,
                prev_ranking_group=prev_ranking_group,
                post=post,
                community=post.community,
                board=post.board,
                point=post.point,
                point_change=post.point - old_point,  # Set point_change
                old_rank=old_rank,
                old_point_rank=old_point_rank
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

        live_badge = Badge.available.get(title='Live Best', model_type='POST')
        weekly_badge = Badge.available.get(title='Weekly Best', model_type='POST')
        monthly_badge = Badge.available.get(title='Monthly Best', model_type='POST')

        # 6. Update post ranking
        for index, ranking in enumerate(ranking_list):
            if new_ranking_group.ranking_type == 'LIVE':
                ranking.post.live_rank = ranking.rank
                ranking.post.live_rank_change = ranking.rank_change

                # 7. Update post badge
                if ranking.post.live_rank < 11 and not ranking.post.badges.filter(id=live_badge.id, is_active=True, is_deleted=False):
                    ranking.post.badges.add(live_badge.id)
                if ranking.post.live_rank > 10 and ranking.post.badges.filter(id=live_badge.id, is_active=True, is_deleted=False):
                    ranking.post.badges.remove(live_badge)

            elif new_ranking_group.ranking_type == 'WEEKLY':
                ranking.post.weekly_rank = ranking.rank
                ranking.post.weekly_rank_change = ranking.rank_change

                if ranking.post.weekly_rank < 11 and not ranking.post.badges.filter(id=weekly_badge.id, is_active=True, is_deleted=False):
                    ranking.post.badges.add(weekly_badge.id)
                if ranking.post.weekly_rank > 10 and ranking.post.badges.filter(id=weekly_badge.id, is_active=True, is_deleted=False):
                    ranking.post.badges.remove(weekly_badge)

            elif new_ranking_group.ranking_type == 'MONTHLY':
                ranking.post.monthly_rank = ranking.rank
                ranking.post.monthly_rank_change = ranking.rank_change

                if ranking.post.monthly_rank < 11 and not ranking.post.badges.filter(id=monthly_badge.id):
                    ranking.post.badges.add(monthly_badge.id)
                if ranking.post.monthly_rank > 10 and ranking.post.badges.filter(id=monthly_badge.id):
                    ranking.post.badges.remove(monthly_badge)

            elif new_ranking_group.ranking_type == 'RISING':
                ranking.post.rising_rank = ranking.rank
                ranking.post.rising_rank_change = ranking.rank_change

            ranking.post.save()

        post_rankings = PostRanking.objects.bulk_create(ranking_list)
        return post_rankings


# Main Section
class PostRanking(Model):
    # FK
    ranking_group = models.ForeignKey('RankingGroup', verbose_name=_('Ranking Group'), on_delete=models.CASCADE,
                                      related_name='post_rankings')
    prev_ranking_group = models.ForeignKey('rankings.RankingGroup', verbose_name=_('Prev Ranking Group'),
                                           on_delete=models.SET_NULL, null=True, blank=True)
    community = models.ForeignKey('communities.Community', verbose_name=_('Community'), on_delete=models.CASCADE,
                                  related_name='post_rankings')
    board = models.ForeignKey('boards.Board', verbose_name=_('Board'), on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='post_rankings')
    post = models.ForeignKey('posts.Post', verbose_name=_('Post'), on_delete=models.CASCADE,
                             related_name='post_rankings')

    # Rank
    rank = models.IntegerField(_('Rank'), default=0)
    old_rank = models.IntegerField(_('Old Rank'), default=0)
    rank_change = models.IntegerField(_('Rank Change'), default=0)

    point_rank = models.IntegerField(_('Point Rank'), default=0)
    old_point_rank = models.IntegerField(_('Old Point Rank'), default=0)
    point_rank_change = models.IntegerField(_('Point Rank Change'), default=0)

    point = models.IntegerField(_('Point'), default=0)
    point_change = models.IntegerField(_('Point Change'), default=0)

    objects = PostRankingManager()

    class Meta:
        verbose_name = verbose_name_plural = _('Post Ranking')
        ordering = ['-created']
