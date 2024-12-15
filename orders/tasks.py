from celery import shared_task
from django.core.mail import send_mail

from R4C import settings


# TODO: ДОЛжен ли я дропать робота из бд?
@shared_task
def send_order_created_email(email: str, serial: str):
    """Заказ создан"""
    send_mail(
        "Заказ R4C",
        f"Ваш заказ на робота {serial} успешно создан!",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
