"""
Base settings to build other settings files upon.
"""

import logging
import os
import urllib.parse
from pathlib import Path
from typing import List

import environ
import sentry_sdk
from corsheaders.defaults import default_headers, default_methods
from django.utils.translation import ugettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# 1. Paths
# ------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "community"
env = environ.Env()

# 2. ENVIRONMENT
# ------------------------------------------------------------------------------
DJANGO_SETTINGS_MODULE = env("DJANGO_SETTINGS_MODULE")
print(f"DJANGO_SETTINGS_MODULE: {DJANGO_SETTINGS_MODULE}")

ENVIRONMENT = DJANGO_SETTINGS_MODULE.split(".")[-1]
print(f"Running server using {ENVIRONMENT} settings")

# 3. Load environment files
# ------------------------------------------------------------------------------
env_files_to_read: List[Path] = []
if ENVIRONMENT == "local":
    local_env_dir = ROOT_DIR / ".envs" / ".local"
    if local_env_dir.exists():
        env_files_to_read.extend(local_env_dir.iterdir())
    READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
    if READ_DOT_ENV_FILE:
        dot_env_file = ROOT_DIR / ".env"
        env_files_to_read.append(dot_env_file)
else:
    django_env_file = ROOT_DIR / ".envs" / f".{ENVIRONMENT}" / ".django"
    env_files_to_read.append(django_env_file)

for f in env_files_to_read:
    if f.exists():
        print(f"Reading environments from {f!s}")
        env.read_env(str(f))
    else:
        print(f"Warning: Environment file does not exist: {f}")

# 4. Service Configuration
# ------------------------------------------------------------------------------
SERVICE_TITLE = env("SERVICE_TITLE", default="COMMUNITY")
SERVICE_PATH = "".join(SERVICE_TITLE.lower().split("_"))

# 5. GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Asia/Seoul"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

LANGUAGES = [
    ("en", "English"),
    ("ko", "Korean"),
    ("ja", "Japanese"),
    ("zh-hans", "Simplified Chinese"),
    ("zh-hant", "Traditional Chinese"),
    ("es", "Spanish"),
    ("ru", "Russian"),
    ("ar", "Arabic"),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = (lang_code for lang_code, lang_name in LANGUAGES)

# 6. DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

if DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
    DATABASES["default"]["OPTIONS"] = {
        "charset": "utf8mb4",
        "use_unicode": True,
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        "isolation_level": "READ COMMITTED",
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 7. URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# 8. INSTALLED APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "modeltranslation",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "phonenumber_field",
    "django_redis",
    "crispy_forms",
    "admin_reorder",
    "django_admin_relation_links",
    "nested_admin",
    "import_export",
    "inline_actions",
    "rangefilter",
    "nested_inline",
    "admin_numeric_filter",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.apple",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_extra_fields",
    "drf_yasg",
    "url_filter",
    "health_check",
    "health_check.db",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
    "django_summernote",
    "django_crontab",
]

LOCAL_APPS = [
    "community.bases.apps.BasesConfig",
    "community.apps.badges.apps.BadgesConfig",
    "community.apps.bans.apps.BansConfig",
    "community.apps.boards.apps.BoardsConfig",
    "community.apps.bookmarks.apps.BookmarksConfig",
    "community.apps.communities.apps.CommunitiesConfig",
    "community.apps.community_medias.apps.CommunityMediasConfig",
    "community.apps.community_posts.apps.CommunityPostsConfig",
    "community.apps.community_users.apps.CommunityUsersConfig",
    "community.apps.comments.apps.CommentsConfig",
    "community.apps.friends.apps.FriendsConfig",
    "community.apps.likes.apps.LikesConfig",
    "community.apps.post_tags.apps.PostTagsConfig",
    "community.apps.posts.apps.PostsConfig",
    "community.apps.profiles.apps.ProfilesConfig",
    "community.apps.rankings.apps.RankingsConfig",
    "community.apps.reports.apps.ReportsConfig",
    "community.apps.shares.apps.SharesConfig",
    "community.apps.tags.apps.TagsConfig",
    "community.apps.users.apps.UsersConfig",
    "community.apps.visits.apps.VisitsConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# 9. MIGRATIONS
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "community.contrib.sites.migrations"}

# 10. AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "account_login"

# 11. PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 12. MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "config.middleware.AutoLoginMiddleware",
]

# 13. STORAGES
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["storages"]  # noqa F405
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"}
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
AWS_S3_CUSTOM_DOMAIN = env("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
STATICFILES_STORAGE = "community.utils.storages.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = f"https://{aws_s3_domain}/static/"
DEFAULT_FILE_STORAGE = "community.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"

# 14. TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "community.utils.context_processors.settings_context",
            ],
        },
    }
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# 15. FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# 16. SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="*").split(" ")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [
    "https://*.superclubs.io",
    "http://*.127.0.0.1",
    "http://*.localhost",
]
CSRF_COOKIE_SAMESITE = None
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "ALLOWALL"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# 18. ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
ADMINS = [("""RUNNERS""", "admin@runners.im")]
MANAGERS = ADMINS

ADMIN_MASTER_REORDER = ("community_users", "boards", "posts", "comments", "rankings")
ADMIN_USER_REORDER = (
    "community_users",
    "boards",
)
ADMIN_REORDER = ADMIN_USER_REORDER

# 19. LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# 20. django-allauth 설정
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)

# 21. django-rest-framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "config.authentication.Authentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/second",
        "user": "50/second",
    },
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": "community.utils.exception_handlers.exception_handler",
    "NON_FIELD_ERRORS_KEY": "non_field_errors",
}

# 22. CORS settings
# ------------------------------------------------------------------------------
original_origins = env("DJANGO_CORS_ALLOWED_ORIGINS", default="").split(",")


def add_www_versions(origins):
    new_origins = set()
    for origin in origins:
        if origin:
            if origin.startswith("https://"):
                new_origins.add(origin)
                if not origin.startswith("https://www."):
                    new_origins.add(origin.replace("https://", "https://www."))
            else:
                new_origins.add(origin)
    return list(new_origins)


CORS_ALLOWED_ORIGINS = add_www_versions(original_origins)
CORS_ALLOW_ALL_ORIGINS = not bool(CORS_ALLOWED_ORIGINS)
CORS_ALLOW_METHODS = default_methods
CORS_ALLOW_HEADERS = default_headers + ("Language-Code",)
CORS_ALLOW_CREDENTIALS = True

# 23. django-health-check
# ------------------------------------------------------------------------------
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,  # in MB
}

# 24. django-phonenumber-field
# ------------------------------------------------------------------------------
PHONENUMBER_DEFAULT_REGION = "KR"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

# 25. django-admin-charts
# ------------------------------------------------------------------------------
ADMIN_CHARTS_NVD3_JS_PATH = "bow/nvd3/build/nv.d3.js"
ADMIN_CHARTS_NVD3_CSS_PATH = "bow/nvd3/build/nv.d3.css"
ADMIN_CHARTS_D3_JS_PATH = "bow/d3/d3.js"

# 26. drf-yasg
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "community.utils.api.schema.CustomAutoSchema",
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "description": _(
                "서버에서 발급한 토큰을 기반으로 한 인증 방식입니다."
                "'Token NTY3ODkwIiwibmFtZSI6I...'와 같이 입력해주세요.<br/>토큰이 세션보다 우선적으로 사용됩니다.<br/>"
            ),
            "name": "Authorization",
            "in": "header",
        },
    },
    "OPERATIONS_SORTER": "method",
    "TAGS_SORTER": "alpha",
}

# 28. Crontab
# ------------------------------------------------------------------------------
CRONJOBS = [
    ("30 * * * *", "config.crons.cron_ranking_group_post_hourly", ">> cron.log"),
    ("* 6 * * *", "config.crons.cron_ranking_group_post_daily", ">> cron.log"),
]

# 29. Celery
# ------------------------------------------------------------------------------
CELERY_DEFAULT_QUEUE = "sqs"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

aws_access_key_id = urllib.parse.quote(f"{AWS_ACCESS_KEY_ID}", safe="")
aws_secret_access_key = urllib.parse.quote(f"{AWS_SECRET_ACCESS_KEY}", safe="")

CELERY_BROKER_URL = f"sqs://{aws_access_key_id}:{aws_secret_access_key}@"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": "ap-northeast-2",
    "visibility_timeout": 3600,
    "polling_interval": 60,
    "CELERYD_PREFETCH_MULTIPLIER": 0,
    "queue_name_prefix": f"clubcategory-{ENVIRONMENT}-",
}

# 30. Redis
# ------------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL")
REDIS_REPLICA_URL = env("REDIS_REPLICA_URL", default=None)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
            "REPLICA_SET": {
                "urls": [f"{REDIS_REPLICA_URL}/1"] if REDIS_REPLICA_URL else [],
            },
            "CONNECTION_POOL_KWARGS": {
                "socket_connect_timeout": 5,
                "socket_timeout": 5,
            },
        },
    }
}

# 31. External API
# ------------------------------------------------------------------------------
SUPERCLUB_SERVER_HOST = env("SUPERCLUB_SERVER_HOST", default="")
SUPERCLUB_API_VERSION = env("SUPERCLUB_API_VERSION", default="v1")
SUPERCLUB_WEB_HOST = env("SUPERCLUB_WEB_HOST", default="")

POST_SERVER_HOST = env("POST_SERVER_HOST", default="")
POST_API_VERSION = env("POST_API_VERSION", default="v1")

# 32. Sentry
# ------------------------------------------------------------------------------
if SENTRY_DSN := env("SENTRY_DSN", default=None):
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,
        event_level=logging.ERROR,
    )
    integrations = [
        sentry_logging,
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        send_default_pii=True,
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.01),
    )

# KAFKA
# ------------------------------------------------------------------------------
KAFKA_BROKER_URLS = env.list("KAFKA_BROKER_URLS")
KAFKA_GROUP_ID = env("KAFKA_GROUP_ID")
KAFKA_SASL_USERNAME = env("KAFKA_SASL_USERNAME")
KAFKA_SASL_PASSWORD = env("KAFKA_SASL_PASSWORD")
