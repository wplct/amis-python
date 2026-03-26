import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.test_settings")
django.setup()
