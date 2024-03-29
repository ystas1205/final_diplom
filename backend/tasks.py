import django_rest_passwordreset
from celery.utils.dispatch import signal
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from product_service.celery import app
from backend.models import ConfirmEmailToken
import logging
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.signals import reset_password_token_created


@app.task
def task_new_user(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
        send_mail(
            f"Password Reset Token for {user.email}",
            token.key,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)


@app.task
def task_password_reset(user_id):

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=user_id)

        send_mail(
            f"Password Reset Token for {user.email}",
            user.password,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)
