import json

from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from robots import services as robots_services
from robots.forms import RobotCreateForm
from robots.tasks import create_excel_robot_report


class GetReportView(View):
    def get(self, request):

        file_name = "robot_report.xlsx"

        task = create_excel_robot_report.delay(file_name)
        task.get(timeout=15)

        response = FileResponse(open(file_name, "rb"), as_attachment=True)
        response["Content-Disposition"] = "attachment; filename=robot_report.xlsx"

        return response


@method_decorator(csrf_exempt, name="dispatch")
class RobotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"message": "incorrect data format"}, status=400)

        form = RobotCreateForm(data)

        if form.is_valid():
            robots_services.create_robot(
                model=form.cleaned_data["model"],
                version=form.cleaned_data["version"],
                created=form.cleaned_data["created"],
            )
            return JsonResponse({"message": "success"}, status=200)
        return JsonResponse({"errors": form.errors}, status=400)
