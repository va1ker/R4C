import openpyxl
from celery import shared_task
from datetime import datetime, timedelta
from django.db.models import Count

from robots.models import Robot

def send_robot_awainting_restock_email():
    """Робота нет, но мы отправим сообщение когда появиться"""
    ...


def send_robot_restock_email():
    """Робот появился, отправляем сообщение одному"""
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
