
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from product_service.celery import app

from backend.models import ConfirmEmailToken
import logging


@app.task
def new_user(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
        send_mail(
            f"Password Reset Token for {settings.EMAIL_HOST_USER}",
            token.key,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)



