from customers.models import Customer


def get_or_create_user_by_email(*, email: str) -> Customer:
    customer, _ = Customer.objects.get_or_create(email=email)
    return customer
