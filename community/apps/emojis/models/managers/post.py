from typing import Union

from django.contrib.auth.models import User
from django.db.models import (
    BooleanField,
    Case,
    Count,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Prefetch,
    QuerySet,
    Value,
    When,
    Window,
)
from django.db.models.functions import Coalesce

from community.bases.models import Manager
from community.utils.queryset import annotate_friend_request_status


class PostEmojiManager(Manager):
    def group_by_emoji(self, post_id: str):
        """
        PostEmoji 데이터를 post로 필터링하고,
        emoji_code 기준으로 그룹화 하고,
        emoji_code 별 카운트를 annotate 합니다.
        """
        return self.filter(post_id=post_id).values("emoji_code").annotate(count=Count("emoji_code")).order_by("-count")

    def filter_by_post_and_emoji(self, post_id: str, emoji_code: Union[str, None], user: User):
        """
        PostEmoji 데이터를 post와 emoji_code로 필터링 합니다.
        """
        filter_data = {"post": post_id}
        if emoji_code:
            filter_data["emoji_code"] = emoji_code

        queryset = (
            self.filter(**filter_data)
            .select_related("user")
            .only(
                "emoji_code",
                "is_deleted",
                "created",
                "user__id",
                "user__username",
                "user__profile_image_url",
                "user__is_deleted",
            )
        )

        return annotate_friend_request_status(queryset, user)

    def get_emoji_user_annotations(self, user: User) -> dict:
        """
        * 이모지와 유저 관련 annotation들을 반환
            - user 이모지 선택 여부
            - postemoji user와 친구 여부
            - 이모지 카운트
            - 유저네임 타입 순서
        """
        from community.apps.friends.models import Friend

        is_selected = (
            Exists(self.filter(post=OuterRef("post__id"), user=user, emoji_code=OuterRef("emoji_code")))
            if user.is_authenticated
            else Value(False, output_field=BooleanField())
        )

        is_friend = (
            Coalesce(Exists(Friend.available.filter(me=user, user=OuterRef("user"))), Value(False))
            if user.is_authenticated
            else Value(False, output_field=BooleanField())
        )

        emoji_count = Window(expression=Count("*"), partition_by=[F("post_id"), F("emoji_code")])

        username_type = Case(
            When(user__username__regex=r"^[A-Z]", then=Value(0)),
            When(user__username__regex=r"^[a-z]", then=Value(1)),
            When(user__username__regex=r"^[가-힣]", then=Value(2)),
            When(user__username__regex=r"^[\u3040-\u30FF]", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )

        return {
            "count": emoji_count,
            "is_selected": is_selected,
            "is_friend": is_friend,
            "username_order": username_type,
        }

    def get_emoji_user_ordered_queryset(self, user: User) -> QuerySet:
        """
        * 이모지와 유저 정보가 정렬된 queryset을 반환
        정렬 순서:
            1. 선택된 이모지
            2. 이모지 카운트
            3. 친구 여부
            4. 유저네임 타입
            5. 유저네임 사전순
            6. 이모지 코드

             post 당 emoji 갯수 많아질 시, post_emojis 쿼리에 .filter 추가 고려.
             WHERE emoji_code in ("request.user 선택한 emoji_code", "post 별 갯수 많은 emoji_code")
        """
        return (
            self.only(
                "emoji_code",
                "created",
                "is_deleted",
                "post__id",
                "user__id",
                "user__username",
                "user__is_deleted",
            )
            .annotate(**self.get_emoji_user_annotations(user))
            .select_related("user")
            .order_by("-is_selected", "-count", "-is_friend", "username_order", "user__username", "emoji_code")
        )

    def get_post_emojis_prefetch(self, user: User) -> Prefetch:
        """
        * 포스트의 이모지와 유저 정보를 포함한 Prefetch 객체를 반환
        """
        return Prefetch(
            "post_emojis", queryset=self.get_emoji_user_ordered_queryset(user), to_attr="prefetched_post_emojis"
        )
