import pytest

from customers.models import Customer
from customers.selectors import get_or_create_user_by_email


@pytest.fixture
def customer_fx():
    email = "test@example.com"
    customer_fx = Customer(email=email)
    customer_fx.save()
    return customer_fx


@pytest.mark.django_db
def test_get_or_create_user_creates__new_customer():
    email = "new_user@example.com"

    assert Customer.objects.count() == 0

    customer = get_or_create_user_by_email(email=email)

    assert customer.email == email
    assert Customer.objects.count() == 1


@pytest.mark.django_db
def test_get_or_create_user_returns__existing_customer(customer_fx: Customer):
    existing_customer = customer_fx

    assert Customer.objects.count() == 1

    customer = get_or_create_user_by_email(email=existing_customer.email)

    assert customer == existing_customer
    assert Customer.objects.count() == 1
