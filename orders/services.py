from customers.models import Customer
from orders.models import Order


def create_order(customer: Customer, serial: str) -> None:
    Order.objects.create(customer=customer, robot_serial=serial)
