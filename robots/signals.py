from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot
from robots.tasks import send_robot_restock_email
from wishlist.models import Wishlist


@receiver(post_save, sender=Robot)
def robot_post_save_handler(sender, instance, **kwargs) -> None:
    """
    Обработчик сигнала post_save для модели Robot.
    """
    wishlist_items = Wishlist.objects.filter(robot_serial=instance.serial)
    for wishlist_item in wishlist_items.iterator():
        email = wishlist_item.customer.email
        model, version = wishlist_item.robot_serial.split("-")
        transaction.on_commit(
            lambda: send_robot_restock_email.delay(
                email=email, model=model, version=version
            )
        )
