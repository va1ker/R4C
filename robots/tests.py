import pytest
from django.test import Client

from customers.models import Customer
from customers.tests import customer_fx
from robots.forms import RobotCreateForm
from robots.models import Robot
from robots.services import create_robot
from wishlist.models import Wishlist


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, status_code",
    [
        ({"model": "R4", "version": "D4", "created": "2024-12-11 00:00:00"}, 200),
        ({"model": "R55", "version": "D4", "created": "2024-12-11 00:00:00"}, 400),
    ],
)
def test_robot_create_endpoint(client, data: dict, status_code: int):
    url = "/api/robots/"

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "data, is_valid",
    [
        ({"model": "R2", "version": "D2", "created": "2024-12-13 00:00:00"}, True),
        (
            {
                "model": "A252",  # len > 2
                "version": "B23511",  # len > 2
                "created": "2024-13-11 00:00:00",  # month > 12
            },
            False,
        ),
    ],
)
def test_robot_create_form_validation(data: dict, is_valid: bool):
    form = RobotCreateForm(data)
    assert form.is_valid() == is_valid


@pytest.mark.django_db
def test_create_robot():
    assert Robot.objects.count() == 0
    model = "R2"
    version = "D2"
    created = "2024-12-13 00:00:00"
    create_robot(model=model, version=version, created=created)
    assert Robot.objects.count() == 1


@pytest.mark.django_db
def test_robot_post_save_handler(mocker, customer_fx: Customer):
    mock_send_robot_restock_email = mocker.patch(
        "robots.signals.send_robot_restock_email.delay"
    )
    Wishlist.objects.create(customer=customer_fx, robot_serial="R2-D2")
    create_robot(model="R2", version="D2", created="2024-12-11 00:00:00")
    mock_send_robot_restock_email.assert_called_once()
