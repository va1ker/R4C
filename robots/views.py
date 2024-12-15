from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
from datetime import datetime

from robots.models import Robot

from robots.forms import RobotCreateForm

from robots import services as robots_services


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
