from django.http import FileResponse
from django.views import View
from robots.tasks import create_excel_robot_report 


class GetReportView(View):
    def get(self, request):
        
        file_name = "robot_report.xlsx"

        task = create_excel_robot_report.delay(file_name)

        task.get(timeout=15)

        response = FileResponse(open(file_name, "rb"), as_attachment=True)
        response["Content-Disposition"] = "attachment; filename=robot_report.xlsx"

        return response
