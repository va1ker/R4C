from django.db import transaction
from django.views.generic.edit import FormView

from customers import selectors as customer_selectors
from orders import services as order_services
from orders import tasks as order_tasks
from orders.forms import OrderForm
from robots import selectors as robot_selectors
from robots import tasks as robots_tasks
from wishlist import services as wishlist_services


class OrderView(FormView):
    template_name = "order.html"
    form_class = OrderForm
    success_url = "/"

    def form_valid(self, form):
        with transaction.atomic():
            customer = customer_selectors.get_or_create_user_by_email(
                email=form.cleaned_data["email"]
            )
            robot_serial = form.cleaned_data["robot_serial"]
            if robot_selectors.is_robot_exists(serial=robot_serial):
                order_services.create_order(customer=customer, serial=robot_serial)
                transaction.on_commit(
                    lambda: order_tasks.send_order_created_email.delay(
                        email=customer.email, serial=robot_serial
                    )
                )
            else:
                wishlist_services.create_wishlist_item(
                    customer=customer, serial=robot_serial
                )
                transaction.on_commit(
                    lambda: robots_tasks.send_robot_awainting_restock_email.delay(
                        email=customer.email, serial=robot_serial
                    )
                )

        return super().form_valid(form)
