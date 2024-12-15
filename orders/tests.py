import pytest

from customers.tests import customer_fx  

from .forms import OrderForm
from .models import Order
from .services import create_order


def test_order_form():
    data = {"email": "test@email.com", "robot_serial": "R2-D2"}
    form = OrderForm(data)
    assert form.is_valid() == True 

    data = {"email": "test", "robot_serial": "R2-D2"}  # bad email
    form = OrderForm(data)
    assert form.is_valid() == False  


@pytest.mark.django_db
def test_create_order(customer_fx):
    serial = "R2-D2"
    assert Order.objects.count() == 0
    create_order(customer_fx, serial)
    assert Order.objects.count() == 1
