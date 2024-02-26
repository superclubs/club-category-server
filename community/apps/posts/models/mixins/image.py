# Python
import requests
from random import randint

# Django
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Third Party
from bs4 import BeautifulSoup
import boto3

# Config
from config.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN


# Function Section
def default_thumbnail_image_path():
    number = randint(1, 7)
    path = f'{settings.MEDIA_URL}community/post/default/{number}.png'
    return path


def default_vote_post_image_path():
    path = f'{settings.MEDIA_URL}community/post/default/vote_post.jpg'
    return path


def is_url_media(url):
    media_formats = (
        # Image
        'image/png', 'image/jpeg', 'image/jpg',
        # GIF
        'image/webp', 'image/gif',
        # Video
        'video/mp4', 'video/x-msvideo', 'video/x-ms-wmv', 'video/quicktime', 'video/x-flv', 'video/x-matroska',
    )
    r = requests.head(url)

    if r.headers['content-type'] in media_formats:
        return True
    return False


def upload_image_to_s3(image_data, s3_key):
    # Upload to S3
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             region_name='ap-northeast-2')
    s3_client.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key, Body=image_data, ContentType='image/jpeg')


def extract_image_from_video(video_url, uuid):
    import cv2
    from urllib.parse import urlparse

    cam = cv2.VideoCapture(video_url)
    success, frame = cam.read()
    if success:
        image_data = cv2.imencode('.jpg', frame)[1].tobytes()
        path = urlparse(video_url).path[1:]
        s3_key = path.rsplit('.', 1)[0] + '.jpg'
        upload_image_to_s3(image_data, s3_key)

        thumbnail_media_url = f'https://{AWS_S3_CUSTOM_DOMAIN}/{s3_key}'
        return thumbnail_media_url
    else:
        raise Exception('Failed to read video frame')


def get_thumbnail_media_url_and_medias_data(content, uuid):
    soup = BeautifulSoup(content, features='html.parser')

    media_tags = soup.find_all(['img', 'video'])

    url_list = []
    thumbnail_media_url = None
    has_thumbnail_attr = False

    for media_tag in media_tags:
        if not media_tag.has_attr('src'):
            continue

        url = media_tag['src']

        # Check valid url
        if is_url_media(url):
            r = requests.head(url)

            if 'video' in r.headers['content-type']:
                _type = 'VIDEO'

            elif 'image' in r.headers['content-type']:
                _type = 'IMAGE'

            else:
                continue

            media = {
                'url': url,
                'type': _type
            }

            # Check Thumbnail attr
            if not has_thumbnail_attr and media_tag.has_attr('thumbnail'):
                if _type == 'VIDEO':
                    thumbnail_media_url = extract_image_from_video(video_url=url, uuid=uuid)

                else:
                    thumbnail_media_url = url

                has_thumbnail_attr = True
                url_list.insert(0, media)

            else:
                url_list.append(media)

    if url_list:
        medias_data = url_list

        # If no thumbnail attr
        if not has_thumbnail_attr:
            if url_list[0]['type'] == 'VIDEO':
                thumbnail_media_url = extract_image_from_video(video_url=url_list[0]['url'], uuid=uuid)

            else:
                thumbnail_media_url = url_list[0]['url']
    else:
        medias_data = None

    return thumbnail_media_url, medias_data


# Main Section
class PostMediaModelMixin(models.Model):
    thumbnail_media_url = models.URLField(_('Thumbnail Media URL'), default=default_thumbnail_image_path)
    medias_data = models.JSONField(_('Medias Data'), default=list)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.id is None and len(self.content) and not self.is_vote:
            thumbnail_media_url, medias_data = get_thumbnail_media_url_and_medias_data(content=self.content,
                                                                                       uuid=self.user.uuid)
            if thumbnail_media_url is not None and medias_data is not None:
                self.thumbnail_media_url = thumbnail_media_url
                self.medias_data = medias_data

        return super(PostMediaModelMixin, self).save(*args, **kwargs)
