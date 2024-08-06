import copy
from random import randint
from urllib.parse import urlparse

import boto3

# Third Party
import cv2
import imageio
import numpy as np

# Python
import requests
from bs4 import BeautifulSoup
from django.conf import settings

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Config
from config.settings.base import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_CUSTOM_DOMAIN,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)


# Function Section
def default_thumbnail_image_path():
    number = randint(1, 7)
    path = f"{settings.MEDIA_URL}{settings.SERVICE_PATH}/post/default/{number}.png"
    return path


def default_vote_post_image_path():
    path = f"{settings.MEDIA_URL}{settings.SERVICE_PATH}/post/default/vote_post.jpg"
    return path


def is_url_media(url):
    media_formats = (
        # Image
        "image/png",
        "image/jpeg",
        "image/jpg",
        # GIF
        "image/webp",
        "image/gif",
        # Video
        "video/mp4",
        "video/x-msvideo",
        "video/x-ms-wmv",
        "video/quicktime",
        "video/x-flv",
        "video/x-matroska",
    )
    r = requests.head(url)

    if r.headers["content-type"] in media_formats:
        return True
    return False


def upload_image_to_s3(image_data, s3_key):
    # Upload to S3
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )
    s3_client.put_object(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=s3_key,
        Body=image_data,
        ContentType="image/jpeg",
    )


def extract_data_from_video(video_url):
    """
    video_url 에서 width, height, duration_millisecond, thumbnail_media_url 이 있는 딕셔너리를 반환합니다.
    """
    cam = cv2.VideoCapture(video_url)
    success, frame = cam.read()
    if success:
        data = dict()

        # 1. 비디오 이미지 추출
        image_data = cv2.imencode(".jpg", frame)[1].tobytes()
        path = urlparse(video_url).path[1:]
        s3_key = path.rsplit(".", 1)[0] + ".jpg"
        data["thumbnail_media_url"] = f"https://{AWS_S3_CUSTOM_DOMAIN}/{s3_key}"

        # 2. 이미지 s3 업로드
        upload_image_to_s3(image_data, s3_key)

        # 3. 비디오 비율
        width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        data["width"] = width
        data["height"] = height

        # 4. 비디오 재생시간
        total_frames = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cam.get(cv2.CAP_PROP_FPS)
        data["duration_millisecond"] = int(total_frames / fps * 1000)

        return data

    else:
        raise Exception("Failed to read video frame")


def extract_resolution_from_image(image_url):
    """
    image_url 에서 width, height를 반환합니다.
    """
    try:
        res = requests.get(image_url)
        # 응답 코드 확인
        res.raise_for_status()

        # 바이트 데이터를 numpy 배열로 변환
        image_data = np.asarray(bytearray(res.content), dtype="uint8")

        # 이미지 데이터를 디코딩
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image data")

        height, width = image.shape[:2]
        return width, height

    # 네트워크 요청 관련 예외 처리
    except requests.RequestException as e:
        print(f"Error fetching the image: {e}")
    # 이미지 데이터 처리 관련 예외 처리
    except ValueError as e:
        print(f"Error processing the image: {e}")
    # 기타 예외 처리
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def extract_resolution_from_gif(gif_url):
    """
    gif_url 에서 width, height를 반환합니다.
    """
    try:
        cap = cv2.VideoCapture(gif_url)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cap.release()

        return width, height

    except Exception as e:
        print("Error:", e)
        return None, None


def get_media_type(response):
    content_type = response.headers.get("Content-Type")
    if content_type in ("image/png", "image/jpeg", "image/jpg", "image/webp"):
        return "IMAGE"
    elif content_type in ("image/gif"):
        return "GIF"
    elif content_type in (
        "video/mp4",
        "video/x-msvideo",
        "video/x-ms-wmv",
        "video/quicktime",
        "video/x-flv",
        "video/x-matroska",
    ):
        return "VIDEO"


def get_thumbnail_media_url_and_medias_data(content):
    soup = BeautifulSoup(content, features="html.parser")

    media_tags = soup.find_all(["img", "video", "jodit-collage-item"])

    url_list = []
    thumbnail_media_url = None
    has_thumbnail_attr = False

    for media_tag in media_tags:
        if not media_tag.has_attr("src"):
            continue

        url = media_tag["src"]

        # Check valid url
        if is_url_media(url):
            response = requests.get(url)
            if response.status_code != 200:
                return None
            media_type = get_media_type(response)

            if media_type == "VIDEO":
                _type = "VIDEO"
                video_data = extract_data_from_video(video_url=url)
                width, height = video_data["width"], video_data["height"]

            elif media_type == "IMAGE":
                _type = "IMAGE"
                width, height = extract_resolution_from_image(image_url=url)

            elif media_type == "GIF":
                _type = "IMAGE"
                width, height = extract_resolution_from_gif(gif_url=url)

            else:
                continue

            media = {
                "url": url,
                "type": _type,
                "width": width,
                "height": height,
                "thumbnail_media_url": None,
                "duration_millisecond": None,
            }

            if _type == "VIDEO":
                media["thumbnail_media_url"] = video_data["thumbnail_media_url"]
                media["duration_millisecond"] = video_data["duration_millisecond"]

            # Check Thumbnail attr
            if not has_thumbnail_attr and media_tag.has_attr("thumbnail"):
                if _type == "VIDEO":
                    thumbnail_media_url = video_data["thumbnail_media_url"]
                else:
                    thumbnail_media_url = url

                has_thumbnail_attr = True
                url_list.insert(0, media)

            else:
                url_list.append(media)

    if url_list:
        medias_data = url_list
        if not thumbnail_media_url:
            thumbnail_media_url = url_list[0].get("url", None)
    else:
        medias_data = None

    return thumbnail_media_url, medias_data


def get_blurred_media_url(media_data):
    # Variables
    media_url = media_data.get("url", None)
    response = requests.get(media_url)
    if response.status_code != 200:
        return None
    media_type = get_media_type(response)

    # Image Download
    if media_type == "IMAGE":
        image_array = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    elif media_type == "VIDEO":
        capture = cv2.VideoCapture(media_url)
        success, frame = capture.read()
        if success:
            image = frame
        else:
            return None

    elif media_type == "GIF":
        image = imageio.mimread(response.content)[0]

    else:
        return None

    # Image Blurring
    if image is not None:
        blurred_image = cv2.GaussianBlur(image, (15, 15), 20)
        white_image = np.full_like(blurred_image, (255, 255, 255), dtype=np.uint8)
        white_blurred_image = cv2.GaussianBlur(white_image, (15, 15), 10)
        blended_image = cv2.addWeighted(blurred_image, 0.7, white_blurred_image, 0.3, 0)

        # Save to S3
        blended_image_data = cv2.imencode(".jpg", blended_image)[1].tobytes()
        path = urlparse(media_url).path[1:].replace("media/common/image/", "").replace("media/common/video/", "")

        s3_key = f"media/common/blurred_image/{path}".rsplit(".", 1)[0] + ".jpg"
        upload_image_to_s3(blended_image_data, s3_key)

        # media_data
        media_data["url"] = f"https://{AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
        media_data["type"] = "IMAGE"

        return media_data
    else:
        return None


# Main Section
class PostMediaModelMixin(models.Model):
    thumbnail_media_url = models.URLField(_("Thumbnail Media URL"), default=default_thumbnail_image_path)
    medias_data = models.JSONField(_("Medias Data"), default=list)

    # Blur
    blurred_thumbnail_media_url = models.URLField(
        _("Blurred Thumbnail Media URL"), default=default_thumbnail_image_path
    )
    blurred_medias_data = models.JSONField(_("Blurred Medias Data"), default=list)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_vote or not len(self.content):
            return super(PostMediaModelMixin, self).save(*args, **kwargs)

        thumbnail_media_url, medias_data = get_thumbnail_media_url_and_medias_data(content=self.content)
        if thumbnail_media_url and medias_data:

            self.thumbnail_media_url = thumbnail_media_url
            self.medias_data = medias_data

            if self.is_secret:
                temp_medias_data = copy.deepcopy(medias_data)
                blurred_medias_data = list()

                for media_data in temp_medias_data:
                    blurred_medias_data += [get_blurred_media_url(media_data)]

                self.blurred_thumbnail_media_url = blurred_medias_data[0].get("url", None)
                self.blurred_medias_data = blurred_medias_data

        return super(PostMediaModelMixin, self).save(*args, **kwargs)
