import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

from django.contrib.auth.models import User

username = "Gloria"
email = "glorianushka@gmail.com"
password = "GLOOisaBaddie"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")