from datetime import datetime, timedelta

import openpyxl
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Count

from R4C import settings
from robots.models import Robot


@shared_task
def send_robot_awainting_restock_email(email: str, serial: str):
    """Робота нет, но мы отправим сообщение когда появиться"""
    send_mail(
        "Заказ R4C",
        f"Ваш заказ на робота {serial} создан, однако его нет в наличии, мы отправим вам сообщение на почту когда он появится!",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@shared_task
def send_robot_restock_email(email: str, model: str, version: str):
    """Робот появился, отправляем сообщение одному"""
    message = (
        "Добрый день!"
        + f"Недавно вы интересовались нашим роботом модели {model} , версии {version}."
        + "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
    )

    send_mail("Заказ R4C", message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    ...


@shared_task
def create_excel_robot_report(file_name: str) -> None:
    """Создать отчет по роботам за неделю"""
    date_now = datetime.now()
    date_week_ago = date_now - timedelta(days=7)

    last_week_robots = (
        Robot.objects.filter(created__range=(date_week_ago, date_now))
        .values("model", "version")
        .annotate(count=Count("id"))
    )

    unique_models = set(last_week_robots.values_list("model", flat=True))

    wb = openpyxl.Workbook()

    del wb["Sheet"]  # Delete default sheet

    for model in unique_models:
        sheet = wb.create_sheet(title=model)
        sheet.append(["Модель", "Версия", "Количество за неделю"])

    for robot in last_week_robots:
        sheet = wb[robot["model"]]
        sheet.append([robot["model"], robot["version"], robot["count"]])

    wb.save(file_name)
    wb.close()
