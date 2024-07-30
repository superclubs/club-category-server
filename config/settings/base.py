# Python
import logging
import os
import urllib.parse
from datetime import timedelta
# Third Party
from pathlib import Path
from typing import List

import environ
# Sentry
import sentry_sdk
from corsheaders.defaults import default_headers, default_methods
# Django
from django.utils.translation import ugettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "community"
env = environ.Env()

# ENVIRONMENT
# ---------------------------------------------------------------------------------
DJANGO_SETTINGS_MODULE = env("DJANGO_SETTINGS_MODULE")
print("DJANGO_SETTINGS_MODULE : ", DJANGO_SETTINGS_MODULE)

DJANGO_ENV = DJANGO_SETTINGS_MODULE.split(".")[-1]  # config.settings.(.+)
print(f"Running server using {DJANGO_ENV} settings")

# If current environment is local, read all files in .envs/.local to make it handy
# of using other environment variables. Also, read .env file by default too.
#
# Note: OS environment variables take precedence over variables from .env
env_files_to_read: List[Path] = []
if DJANGO_ENV == "local":
    local_env_dir = ROOT_DIR / ".envs" / ".local"
    if local_env_dir.exists():
        env_files_to_read.extend(local_env_dir.iterdir())

    READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
    if READ_DOT_ENV_FILE:
        dot_env_file = ROOT_DIR / ".env"
        env_files_to_read.append(dot_env_file)
else:
    # Read only necessary file for non-local environment.
    django_env_file = ROOT_DIR / ".envs" / f".{DJANGO_ENV}" / ".django"
    env_files_to_read.append(django_env_file)

files_not_exist = []
for f in env_files_to_read:
    if f.exists():
        print(f"Reading environments from {f!s}")
        env.read_env(str(f))
    else:
        files_not_exist.append(f)

if files_not_exist:
    print("{} file(s) does not exists: {}".format(len(files_not_exist), ", ".join(map(str, files_not_exist))))

print("")

SERVICE_TITLE = env("SERVICE_TITLE", default="COMMUNITY")
SERVICE_PATH = "".join(SERVICE_TITLE.lower().split("_"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Asia/Seoul"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

LANGUAGES = [
    ("en", "English"),
    ("ko", "Korean"),
    ("ja", "Japanese"),
    ("zh-hans", "Simplified Chinese"),  # 간체 중국어
    ("zh-hant", "Traditional Chinese"),  # 번체 중국어
    ("es", "Spanish"),
    ("ru", "Russian"),
    ("ar", "Arabic"),
]

# Model Translation
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = (lang_code for lang_code, lang_name in LANGUAGES)

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

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

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

print("DATABASES : ", DATABASES)

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
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
    "rest_framework_simplejwt",
    # Django Model
    "phonenumber_field",
    "django_redis",
    # Django Form
    "crispy_forms",
    # Django Admin
    "admin_reorder",
    "django_admin_relation_links",
    "nested_admin",
    "import_export",
    "inline_actions",
    "rangefilter",
    "nested_inline",
    "admin_numeric_filter",
    # django-allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.apple",
    # django-rest-framework
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_extra_fields",
    "drf_yasg",
    "url_filter",
    # django-health-check
    "health_check",
    "health_check.db",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
    # Editor
    "django_summernote",
    # Crontab
    "django_crontab",
]

LOCAL_APPS = [
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
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "community.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    # {'NAME': 'community.utils.validators.CustomPasswordValidator'},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "config.middleware.AutoLoginMiddleware"
]

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
AWS_S3_CUSTOM_DOMAIN = env("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# STATIC
# ------------------------
STATICFILES_STORAGE = "community.utils.storages.StaticRootS3Boto3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = f"https://{aws_s3_domain}/static/"
# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "community.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
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

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""RUNNERS""", "admin@runners.im")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

ADMIN_MASTER_REORDER = (
    "community_users",
    "boards",
    "posts",  # Master 계정 전용
    "comments",  # Master 계정 전용
    "rankings"  # Master 계정 전용
)

ADMIN_USER_REORDER = (
    "community_users",
    "boards",
)

ADMIN_REORDER = ADMIN_USER_REORDER

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
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
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "community.apps.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
ACCOUNT_FORMS = {"signup": "community.apps.users.forms.UserSignupForm"}
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "community.apps.users.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
SOCIALACCOUNT_FORMS = {"signup": "community.apps.users.forms.UserSocialSignupForm"}
SILENCED_SYSTEM_CHECKS = ["auth.W004"]

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "config.authentication.Authentication",  # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": "community.utils.exception_handlers.exception_handler",
    "NON_FIELD_ERRORS_KEY": "non_field_errors",
}
# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
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

if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = default_methods
CORS_ALLOW_HEADERS = default_headers + ("Language-Code",)
CORS_ALLOW_CREDENTIALS = True

# Your stuff...
# ------------------------------------------------------------------------------

# django-health-check
# ------------------------------------------------------------------------------------
# https://pypi.org/project/django-health-check/
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,  # in MB
}

# django-phonenumber-field
# --------------------------------------------------------------------------------
# https://github.com/stefanfoulis/django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = "KR"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

# django-admin-charts
# ------------------------------------------------------------------------------
ADMIN_CHARTS_NVD3_JS_PATH = "bow/nvd3/build/nv.d3.js"
ADMIN_CHARTS_NVD3_CSS_PATH = "bow/nvd3/build/nv.d3.css"
ADMIN_CHARTS_D3_JS_PATH = "bow/d3/d3.js"

# drf-yasg
# ------------------------------------------------------------------------------------
# https://drf-yasg.readthedocs.io/en/stable/settings.html
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "community.utils.api.schema.CustomAutoSchema",
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "description": _(
                """서버에서 발급한 토큰을 기반으로 한 인증 방식입니다. 'Token NTY3ODkwIiwibmFtZSI6I...'와 같이 입력해주세요.<br/>
                   토큰이 세션보다 우선적으로 사용됩니다.<br/>"""
            ),
            "name": "Authorization",
            "in": "header",
        },
    },
    "OPERATIONS_SORTER": "method",
    "TAGS_SORTER": "alpha",
}

private_key = open(BASE_DIR + "/private_key.pem", "rb").read()
public_key = open(BASE_DIR + "/public_key.pem", "rb").read()

# django-rest-framework-simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "RS256",
    "SIGNING_KEY": private_key,
    # 'SIGNING_KEY': env('SIGNING_KEY', default=None).encode('ascii'),
    "VERIFYING_KEY": public_key,
    # 'VERIFYING_KEY': env('VERIFYING_KEY', default=None).encode('ascii'),
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    # 'USER_ID_CLAIM': 'user_id',
    "USER_ID_CLAIM": "account_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # 'TOKEN_TYPE_CLAIM': 'token_type',
    "TOKEN_TYPE_CLAIM": None,
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": None,
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Crontab
# ------------------------------------------------------------------------------------
CRONJOBS = [
    # 매 시 30분 실행
    ("30 * * * *", "config.crons.cron_ranking_group_post_hourly", ">> cron.log"),
    # 매일 오전 6시 실행
    ("* 6 * * *", "config.crons.cron_ranking_group_post_daily", ">> cron.log"),
]

# Celery
CELERY_DEFAULT_QUEUE = "sqs"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

# Credentials
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY", default=None)
aws_access_key_id = urllib.parse.quote(f"{AWS_ACCESS_KEY_ID}", safe="")
aws_secret_access_key = urllib.parse.quote(f"{AWS_SECRET_ACCESS_KEY}", safe="")

# Celery
CELERY_BROKER_URL = f"sqs://{aws_access_key_id}:{aws_secret_access_key}@"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": "ap-northeast-2",
    "visibility_timeout": 3600,
    "polling_interval": 60,
    "CELERYD_PREFETCH_MULTIPLIER": 0,
}
# "AWS": "arn:aws:iam::543061907465:root"
CELERY_TASK_DEFAULT_QUEUE = "sqs"

# Redis
REDIS_URL = env("REDIS_URL", default=None)
REDIS_REPLICA_URL = env("REDIS_REPLICA_URL", default=None)

if REDIS_URL:
    # 캐시 설정
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"{REDIS_URL}/5",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
                "REPLICA_SET": {
                    "urls": [f"{REDIS_REPLICA_URL}/5"] if REDIS_REPLICA_URL else [],
                },
            },
        }
    }

# External API
SUPERCLUB_SERVER_HOST = env("SUPERCLUB_SERVER_HOST", default="")
SUPERCLUB_API_VERSION = env("SUPERCLUB_API_VERSION", default="v1")
SUPERCLUB_WEB_HOST = env("SUPERCLUB_WEB_HOST", default="")

POST_SERVER_HOST = env("POST_SERVER_HOST", default="")
POST_API_VERSION = env("POST_API_VERSION", default="v1")

# Sentry
# ------------------------------------------------------------------------------
if SENTRY_DSN := env("SENTRY_DSN", default=None):
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
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
        # environment=env("SENTRY_ENVIRONMENT", default="develop"),
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=1.0),
    )

# Creta
# ------------------------------------------------------------------------------------
CRETA_AUTH_BASE_URL = env("CRETA_AUTH_BASE_URL")
