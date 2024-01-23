# Django
from django.db import models
from django.db.models import Q

# Models
from community.apps.tags.models.index import Tag
from community.apps.post_tags.models.index import PostTag


# Main Section
class PostTagModelMixin(models.Model):
    class Meta:
        abstract = True

    def create_post_tag(self, index, tag):
        tag, created = Tag.available.get_or_create(title=tag.lower().replace(' ', ''))
        post_tag, created = PostTag.available.get_or_create(post=self, tag=tag)
        post_tag.update(order=index, title=tag.title)

    def update_post_tag(self, tags):
        PostTag.available.filter(post=self).filter(~Q(tag__title__in=tags)).soft_delete()
        for index, tag in enumerate(tags):
            tag, created = Tag.available.get_or_create(title=tag.lower().replace(' ', ''))
            if created:
                print('[Post] update_post_tag', tag, '생성')
            post_tag, created = PostTag.available.get_or_create(post=self, tag=tag)
            post_tag.update(order=index, title=tag.title)
