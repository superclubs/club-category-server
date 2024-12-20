
from django.contrib.auth.models import User
from django.db.models import (
    Case,
    CharField,
    Exists,
    OuterRef,
    Prefetch,
    QuerySet,
    Subquery,
    Value,
    When,
)

from community.apps.friends.models import Friend, FriendRequest
from community.modules.choices import FRIEND_REQUEST_AVAILABLE_STATUS


def annotate_friend_request_status(queryset: QuerySet, user: User) -> QuerySet:
    """
    주어진 QuerySet 에 friend_request_status 및 friend_request_id를 annotate.
    """
    if not user.is_authenticated:
        return queryset

    prefetch_user_friends = Friend.available.filter(user=user)

    send_friend_request_subquery = FriendRequest.available.filter(
        sender=user,
        receiver=OuterRef("user"),
    ).values("status")

    receive_friend_request_subquery = FriendRequest.available.filter(
        sender=OuterRef("user"),
        receiver=user,
    ).values("status", "id")

    return queryset.prefetch_related(Prefetch("user__my_friends", queryset=prefetch_user_friends)).annotate(
        friend_request_status=Case(
            When(
                Exists(send_friend_request_subquery.filter(status=FRIEND_REQUEST_AVAILABLE_STATUS.APPROVED)),
                then=Value(FRIEND_REQUEST_AVAILABLE_STATUS.APPROVED),
            ),
            When(
                Exists(receive_friend_request_subquery.filter(status=FRIEND_REQUEST_AVAILABLE_STATUS.APPROVED)),
                then=Value(FRIEND_REQUEST_AVAILABLE_STATUS.APPROVED),
            ),
            When(Exists(send_friend_request_subquery), then=Value(FRIEND_REQUEST_AVAILABLE_STATUS.SEND)),
            When(
                Exists(receive_friend_request_subquery.filter(status="PENDING")),
                then=Value(FRIEND_REQUEST_AVAILABLE_STATUS.RECEIVED),
            ),
            default=Value(None),
            output_field=CharField(),
        ),
        friend_request_id=Case(
            When(
                Exists(receive_friend_request_subquery.filter(status="PENDING")),
                then=Subquery(receive_friend_request_subquery.values("id")[:1]),
            ),
            default=Value(None),
            output_field=CharField(),
        ),
    )
