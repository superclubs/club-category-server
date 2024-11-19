# Django
from django.urls import include, path

# DRF
from rest_framework_nested import routers

# Board
from community.apps.boards.api.views import (
    BoardAdminViewSet,
    BoardViewSet,
    CommunityBoardsAdminViewSet,
    CommunityBoardsViewSet,
)

# Comment
from community.apps.comments.api.views import CommentsViewSet, CommentViewSet

# Community
from community.apps.communities.api.views import (
    CommunitiesViewSet,
    CommunityAdminViewSet,
    CommunityViewSet,
)

# Like
from community.apps.likes.api.views import CommentLikesViewSet, PostLikesViewSet

# Post
from community.apps.posts.api.views import (
    BoardPostsViewSet,
    CommunityPostsViewSet,
    PostsViewSet,
    PostViewSet,
)

# User
from community.apps.users.api.views import UserAdminViewSet, UsersViewSet, UserViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# User Section
router.register("users", UsersViewSet)
router.register("admin/user", UserAdminViewSet)

# Community Section
router.register("communities", CommunitiesViewSet)

# Community Admin Section
router.register("admin/community", CommunityAdminViewSet)

# Post Section
router.register(r"posts", PostsViewSet, basename="posts")

# Comment Section
router.register("comment", CommentViewSet)

# Board Admin Section
router.register("admin/board", BoardAdminViewSet)

# Nested Router Section
# User Nested Router
router.register(r"user", UserViewSet, basename="user")

# Community Nested Router
router.register(r"community", CommunityViewSet, basename="community")
community_posts_router = routers.NestedSimpleRouter(router, r"community", lookup="community")
community_posts_router.register(r"posts", CommunityPostsViewSet, basename="community-posts")
community_boards_router = routers.NestedSimpleRouter(router, r"community", lookup="community")
community_boards_router.register(r"boards", CommunityBoardsViewSet, basename="community-boards")
community_boards_admin_router = routers.NestedSimpleRouter(router, r"admin/community", lookup="community")
community_boards_admin_router.register(r"boards", CommunityBoardsAdminViewSet, basename="community-boards")

# Board Nested Router
router.register(r"board", BoardViewSet, basename="board")
board_posts_router = routers.NestedSimpleRouter(router, r"board", lookup="board")
board_posts_router.register(r"posts", BoardPostsViewSet, basename="board-posts")

# Post Nested Router
router.register(r"post", PostViewSet, basename="post")
post_comments_router = routers.NestedSimpleRouter(router, r"post", lookup="post")
post_comments_router.register(r"comments", CommentsViewSet, basename="post-comments")
post_likes_router = routers.NestedSimpleRouter(router, r"post", lookup="post")
post_likes_router.register(r"likes", PostLikesViewSet, basename="post-likes")

# Comment Nested Router
router.register(r"comment", CommentViewSet, basename="comment")
comment_likes_router = routers.NestedSimpleRouter(router, r"comment", lookup="comment")
comment_likes_router.register(r"likes", CommentLikesViewSet, basename="comment-likes")

app_name = "api"
urlpatterns = [
    path("", include("community.apps.users.urls")),
    path("", include(community_boards_router.urls)),
    path("", include(community_boards_admin_router.urls)),
    path("", include(community_posts_router.urls)),
    path("", include(board_posts_router.urls)),
    path("", include(post_comments_router.urls)),
    path("", include(post_likes_router.urls)),
    path("", include(comment_likes_router.urls)),
] + router.urls
