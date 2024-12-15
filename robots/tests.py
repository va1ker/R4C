import pytest
from django.test import Client

from .forms import RobotCreateForm
from .models import Robot
from .services import create_robot


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_robot_create_endpoint(client):
    url = "/api/robots/"
    data = {"model": "R4", "version": "D4", "created": "2024-12-11 00:00:00"}

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}

    data = {"model": "R55", "version": "D4", "created": "2024-12-11 00:00:00"}

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400


def test_robot_create_form_validation():
    data = {"model": "R2", "version": "D2", "created": "2024-12-13 00:00:00"}
    form = RobotCreateForm(data)
    assert form.is_valid() == True
    data = {
        "model": "A252",  # len > 2
        "version": "B23511",  # len > 2
        "created": "2024-13-11 00:00:00",  # month > 12
    }
    form = RobotCreateForm(data)
    assert form.is_valid() == False


@pytest.mark.django_db
def test_create_robot():
    assert Robot.objects.count() == 0
    model = "R2"
    version = "D2"
    created = "2024-12-13 00:00:00"
    create_robot(model=model, version=version, created=created)
    assert Robot.objects.count() == 1
