from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot

from wishlist.models import Wishlist

from robots.tasks import send_robot_restock_email


@receiver(post_save, sender=Robot)
def robot_post_save_handler(sender, instance, **kwargs) -> None:
    """
    Обработчик сигнала post_save для модели Robot.
    """
    wishlist_item = Wishlist.objects.filter(robot_serial=instance.serial).first()
    if wishlist_item:
        model, version = wishlist_item.robot_serial.split("-")
        send_robot_restock_email.delay(
            email=wishlist_item.customer.email, model=model, version=version
        )
