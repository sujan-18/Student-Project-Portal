from django.conf import settings

if not settings.configured:
    settings.configure()

from django.contrib.auth.hashers import check_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return check_password(plain_password, hashed_password)
