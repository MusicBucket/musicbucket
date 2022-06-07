from functools import partial

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

from configurations import Configuration
from kaio import Options, mixins

opts = Options()
get = partial(opts.get, section="Database")


class Base(
    mixins.CachesMixin,
    mixins.DatabasesMixin,
    mixins.CompressMixin,
    mixins.PathsMixin,
    mixins.LogsMixin,
    mixins.EmailMixin,
    mixins.SecurityMixin,
    mixins.DebugMixin,
    mixins.WhiteNoiseMixin,
    mixins.StorageMixin,
    Configuration,
):
    """
    Project settings for development and production.
    """

    DEBUG = opts.get("DEBUG", True)

    BASE_DIR = opts.get("APP_ROOT", None)
    APP_SLUG = opts.get("APP_SLUG", "musicbucket")
    SITE_ID = 1
    SECRET_KEY = opts.get("SECRET_KEY", "key")

    # Since Django 3.2 is: DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    # ref: https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # django-cors-headers
    CORS_ALLOW_ALL_ORIGINS = True

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = "en"
    LANGUAGES = (
        ("en", _("English")),
        ("es", _("Spanish")),
    )
    TIME_ZONE = "Europe/Madrid"

    ROOT_URLCONF = "main.urls"
    WSGI_APPLICATION = "main.wsgi.application"

    INSTALLED_APPS = [
        # django
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # apps
        "main",
        "api",
        "profiles",
        "telegram",
        "spotify",
        "lastfm",
        "web",
        "app",
        # 3rd parties
        "django_rq",
        "rest_framework",
        "rest_framework_simplejwt",
        "rest_framework.authtoken",
        "django_filters",
        "compressor",
        "constance",
        "constance.backends.database",
        "django_extensions",
        "kaio",
        "robots",
        "storages",
        "widget_tweaks",
        "django_telegram_login",
        "django_tables2",
        "crispy_forms",
        "hijack",
        "cookielaw",
        "corsheaders",
    ]

    # HEALTH_CHECK_APPS = [
    #     'health_check',
    #     'health_check.db',
    #     # stock Django health checkers
    #     'health_check.cache',
    #     # 'health_check.storage',
    #     # 'health_check.contrib.celery',
    #     # 'health_check.contrib.s3boto3_storage',
    # ]
    #
    # INSTALLED_APPS += HEALTH_CHECK_APPS

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # SecurityMiddleware options
    SECURE_BROWSER_XSS_FILTER = True

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                # insert additional TEMPLATE_DIRS here
            ],
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.tz",
                    "django.template.context_processors.request",
                    "constance.context_processors.config",
                ],
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
            },
        },
    ]
    if not DEBUG:
        TEMPLATES[0]["OPTIONS"]["loaders"] = [
            (
                "django.template.loaders.cached.Loader",
                TEMPLATES[0]["OPTIONS"]["loaders"],
            ),
        ]


    # Bootstrap 3 alerts integration with Django messages
    MESSAGE_TAGS = {
        messages.ERROR: "danger",
    }

    # Sessions
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

    LOGIN_URL = "profiles:login"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_REDIRECT_URL = "profiles:login"

    DEFAULT_FROM_EMAIL = opts.get("DEFAULT_FROM_EMAIL", "no-reply@musicbucket.net")

    # Celery
    DJANGO_CELERY_QUEUES = opts.get("DJANGO_CELERY_QUEUES", "musicbucket")

    # Constance
    CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
    CONSTANCE_DATABASE_CACHE_BACKEND = "default"
    CONSTANCE_CONFIG = {
        "GOOGLE_ANALYTICS_TRACKING_CODE": (
            "UA-XXXXX-Y",
            "Google Analytics tracking code.",
        ),
    }

    # Robots
    ROBOTS_SITEMAP_URLS = [opts.get("SITEMAP_URL", "")]

    # pgBouncer
    # https://docs.djangoproject.com/en/2.1/ref/databases/#transaction-pooling-server-side-cursors
    # DISABLE_SERVER_SIDE_CURSORS = True

    # Google Recaptcha (django-recaptcha)
    RECAPTCHA_PUBLIC_KEY = opts.get("RECAPTCHA_PUBLIC_KEY", "")
    RECAPTCHA_PRIVATE_KEY = opts.get("RECAPTCHA_PRIVATE_KEY", "")

    # django-hijack
    HIJACK_LOGIN_REDIRECT_URL = (
        "/"  # Where admins are redirected to after hijacking a user
    )
    HIJACK_LOGOUT_REDIRECT_URL = (
        "/admin/auth/user/"  # Where admins are redirected to after releasing a user
    )
    HIJACK_ALLOW_GET_REQUESTS = True

    # Rest Framework
    REST_FRAMEWORK = {
        "DEFAULT_FILTER_BACKENDS": (
            "django_filters.rest_framework.DjangoFilterBackend",
        ),
        "DEFAULT_PERMISSION_CLASSES": [],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ),
        #"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        #"PAGE_SIZE": 100
    }

    # RQ
    RQ_SHOW_ADMIN_LINK = True

    RQ_QUEUES = {
        "default": {
            "HOST": opts.get("REDIS_HOST", "localhost"),
            "PORT": opts.get("REDIS_PORT", 6379, int),
            "DB": opts.get("REDIS_DB", 0, int),
            "PASSWORD": "",
            "DEFAULT_TIMEOUT": 12000,
        }
    }

    # LastFM
    LASTFM_API_KEY = opts.get("LASTFM_API_KEY")
    LASTFM_API_SECRET = opts.get("LASTFM_API_SECRET")

    # Spotify
    SPOTIFY_CLIENT_ID = opts.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = opts.get("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = opts.get("SPOTIFY_REDIRECT_URI")

    # Telegram
    TELEGRAM_BOT_NAME = opts.get("TELEGRAM_BOT_NAME")
    TELEGRAM_BOT_TOKEN = opts.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_LOGIN_REDIRECT_URL = opts.get("TELEGRAM_LOGIN_REDIRECT_URL")


class Test(Base):
    """
    Project settings for testing.
    """

    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

    MEDIA_ROOT = opts.get("TEST_MEDIA_ROOT", "/tmp/musicbucket-media_test")

    CACHE_PREFIX = "musicbucket-test"

    SESSION_ENGINE = "django.contrib.sessions.backends.db"

    def DATABASES(self):
        return self.get_databases(prefix="TEST_")
