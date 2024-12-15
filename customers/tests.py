import pytest

from .models import Customer
from .selectors import get_or_create_user_by_email


@pytest.fixture
def customer_fx():
    email = "test@example.com"
    customer_fx = Customer(email=email)
    customer_fx.save()
    return customer_fx


@pytest.mark.django_db
def test_get_or_create_user_creates_new_customer():
    email = "new_user@example.com"

    assert Customer.objects.filter(email=email).count() == 0

    customer = get_or_create_user_by_email(email=email)

    assert customer.email == email
    assert Customer.objects.filter(email=email).count() == 1


@pytest.mark.django_db
def test_get_or_create_user_returns_existing_customer(customer_fx):
    existing_customer = customer_fx

    assert Customer.objects.filter(email=existing_customer.email).count() == 1

    customer = get_or_create_user_by_email(email=existing_customer.email)

    assert customer == existing_customer
    assert Customer.objects.filter(email=existing_customer.email).count() == 1
