#!/bin/sh
set -e

mkdir -p "${DJANGO_DATA_DIR:-/app/data}" "${DJANGO_STATIC_ROOT:-/app/staticfiles}" "${DJANGO_MEDIA_ROOT:-/app/media}"

python manage.py check

if [ "${DJANGO_RUN_MIGRATIONS:-1}" = "1" ]; then
    python manage.py migrate --noinput
fi

if [ "${DJANGO_COLLECTSTATIC:-1}" = "1" ]; then
    python manage.py collectstatic --noinput
fi

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell <<'PY'
import os

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

user, created = User.objects.get_or_create(
    username=username,
    defaults={"email": email, "is_staff": True, "is_superuser": True},
)

if created:
    user.set_password(password)
    user.save(update_fields=["password"])
else:
    changed = False
    if not user.is_staff:
        user.is_staff = True
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True
    if email and user.email != email:
        user.email = email
        changed = True
    if changed:
        user.save()
PY
fi

exec "$@"
