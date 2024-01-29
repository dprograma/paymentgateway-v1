
from paymentgateway.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "d976bc0aee1758e18cdfe7bd8cd2b99b84d2dc4b1f0262b1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


