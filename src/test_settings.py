# test_settings.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'your-secret-key-for-testing-only'
DEBUG = True
USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",  # 如果你的模型用了 User
    "django.contrib.sessions",
    "amis_python",          # 你的 app
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

ROOT_URLCONF = "test_urls"
