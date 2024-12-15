from customers.models import Customer
from wishlist.models import Wishlist


def create_wishlist_item(customer: Customer, serial: str) -> None:
    Wishlist.objects.create(customer=customer, robot_serial=serial)
