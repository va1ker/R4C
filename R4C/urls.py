"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from orders.views import OrderSuccessView, OrderView
from robots.views import GetReportView, RobotView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/robots/", RobotView.as_view()),
    path("report/", GetReportView.as_view()),
    path("order/", OrderView.as_view()),
    path("order_success/", OrderSuccessView.as_view(), name="order_success"),
]
