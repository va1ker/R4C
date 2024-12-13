from django.http import FileResponse
from django.views import View
from datetime import datetime, timedelta

from robots.models import Robot
from django.db.models import Count


import openpyxl


class GetReportView(View):
    def get(self, request):
        # TODO:Move to celery?

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

        excel = "robot_report.xlsx"
        wb.save(excel)
        wb.close()

        response = FileResponse(open(excel, "rb"), as_attachment=True)
        response["Content-Disposition"] = "attachment; filename=robot_report.xlsx"

        return response
