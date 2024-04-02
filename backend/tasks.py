import yaml
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django_rest_passwordreset.models import ResetPasswordToken
from product_service.celery import app
from backend.models import ConfirmEmailToken, User, Shop, Category, \
    ProductParameter, Parameter, ProductInfo, Product


@app.task
def task_new_user(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
        send_mail(
            # title:
            f"Password Reset Token for {user.email}",
            # message:
            token.key,
            settings.EMAIL_HOST_USER,
            # from:
            [user.email],
            # to:
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)
    return 'Done'


@app.task
def task_password_reset(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        key = [data.key for data in ResetPasswordToken.objects.all()]

        send_mail(
            # title:
            f"Password Reset Token for {user}",
            # message:
            ''.join(key),
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)
    return 'Done'


@app.task
def task_new_order(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)

        send_mail(
            # title:
            f"Обновление статуса заказа",
            # message:
            'Заказ сформирован',
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user '%s'" % user_id)
    return 'Done'


@app.task
def task_product_export(user_id):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=user_id)
    datas = Shop.objects.filter(state=True,
                                user_id=user.id, ).prefetch_related(
        'categories__products__product_infos__product_parameters__parameter')
    if datas:
        list_category = []
        list_goods = []
        for shops in datas:
            shop = shops.name
            for category in shops.categories.all():
                list_category.append({
                    'id': category.id,
                    'name': category.name
                })

                for product in category.products.all():
                    for product_info in product.product_infos.all():
                        dict_parameter = {}
                        for par in product_info.product_parameters.all():
                            dict_parameter.update(
                                {par.parameter.name: par.value})

                        list_goods.append({
                            'category': product.category_id,
                            'name': product.name,
                            'model': product_info.price,
                            'id': product_info.external_id,
                            'price': product_info.price,
                            'price_rrc': product_info.price_rrc,
                            'quantity': product_info.quantity,
                            'parameter': dict_parameter,

                        })

        data = {
            'shop': shop,
            'category': list_category,
            'goods': list_goods,
        }

        with open("product.yaml", "a", encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, sort_keys=False)
        return 'Done'


@app.task
def task_product_import(user_id):
    pass
