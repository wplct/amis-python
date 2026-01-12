# test_settings.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'your-secret-key-for-testing-only'
DEBUG = True
USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",  # 如果你的模型用了 User
    "amis_python",          # 你的 app
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# 如果你的 app 用了 URL 或模板，可能还需要：
ROOT_URLCONF = "amis_python.urls"  # 如果有 urls.py，否则可省略