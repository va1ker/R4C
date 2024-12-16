import pytest

from customers.models import Customer
from customers.tests import customer_fx
from orders.forms import OrderForm
from orders.models import Order
from orders.services import create_order


@pytest.mark.parametrize(
    "data, is_valid",
    [
        ({"email": "test@email.com", "robot_serial": "R2-D2"}, True),
        ({"email": "test", "robot_serial": "R2-D2"}, False),  # bad email
    ],
)
def test_order_form(data: dict, is_valid: bool):
    form = OrderForm(data)
    assert form.is_valid() == is_valid


@pytest.mark.django_db
def test_create_order(customer_fx: Customer):
    serial = "R2-D2"
    assert Order.objects.count() == 0
    create_order(customer_fx, serial)
    assert Order.objects.count() == 1
