from django.core.management.base import BaseCommand


# Main Section
class Command(BaseCommand):
    help = "Like 데이터를 Emoji로 변환 하는 명령어, community/post/comment/profile signal 로직 주석하고 실행해주세요"

    def add_arguments(self, parser):
        parser.add_argument("--model", type=str, required=True, help="post_emoji | comment_emoji")

    def handle(self, *args, **options):
        from community.apps.emojis.models import CommentEmoji, PostEmoji
        from community.apps.likes.models import CommentLike, PostLike

        model = options["model"]
        if model not in ("post_emoji", "comment_emoji"):
            self.stdout.write(self.style.ERROR(f"invalid --model option"))

        emoji_dict = {"LIKE": "😍", "FUN": "😆", "HEALING": "😌", "LEGEND": "😎", "USEFUL": "😉", "EMPATHY": "😲"}

        if model == "post_emoji":
            post_likes = PostLike.available.all()
            for post_like in post_likes:
                emoji_code = emoji_dict.get(post_like.type)
                if not emoji_code:
                    print(f"생성 제외: post={post_like.post}, {post_like.type}")
                    continue

                try:
                    # Post 존재 여부 확인
                    post = post_like.post
                    user = post_like.user
                    profile = post_like.profile

                    # PostEmoji 생성 또는 업데이트
                    post_emoji = PostEmoji.objects.filter(post=post, user=user).first()
                    if post_emoji:
                        print(f"생성 제외: {user}는 이미 {post}에 {post_emoji.emoji_code}를 생성하였습니다.")
                        continue
                    else:
                        PostEmoji.objects.create(
                            post=post, user=user, emoji_code=emoji_code, profile=profile, created=post_like.created
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"생성 완료: post={post}, user={user}, type={post_like.type} -> emoji={emoji_code}"
                        )
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing PostLike={post_like}: {str(e)}"))

            self.stdout.write(self.style.SUCCESS("Convert migration completed successfully"))

        elif model == "comment_emoji":
            comment_likes = CommentLike.available.all()
            for comment_like in comment_likes:
                emoji_code = emoji_dict.get(comment_like.type)
                if not emoji_code:
                    print(f"생성 제외: comment={comment_like.comment}, {comment_like.type}")
                    continue

                try:
                    # Comment 존재 여부 확인
                    comment = comment_like.comment
                    user = comment_like.user
                    profile = comment_like.profile

                    # CommentEmoji 생성 또는 업데이트
                    comment_emoji = CommentEmoji.objects.filter(comment=comment, user=user).first()
                    if comment_emoji:
                        print(f"생성 제외: {user}는 이미 {comment}에 {comment_emoji.emoji_code}를 생성하였습니다.")
                        continue
                    else:
                        CommentEmoji.objects.create(
                            comment=comment,
                            user=user,
                            profile=profile,
                            emoji_code=emoji_code,
                            created=comment_like.created,
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"생성 완료: comment={comment}, user={user}, type={comment_like.type} -> emoji={emoji_code}"
                        )
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing CommentLike={comment_like}: {str(e)}"))

            self.stdout.write(self.style.SUCCESS("Convert migration completed successfully"))
