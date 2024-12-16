import pytest

from customers.models import Customer
from customers.tests import customer_fx
from wishlist.models import Wishlist
from wishlist.services import create_wishlist_item


@pytest.mark.django_db
def test_wishlist_creation(customer_fx: Customer):
    assert Wishlist.objects.count() == 0
    serial = "R2-D2"
    create_wishlist_item(customer_fx, serial)
    assert Wishlist.objects.count() == 1
    wishlist = Wishlist.objects.get(customer=customer_fx)
    assert wishlist.robot_serial == serial
