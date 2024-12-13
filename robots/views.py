from django.views import View
from django.http import JsonResponse

import json
from datetime import datetime

from robots.models import Robot

class RobotView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if ("model" and "version" and "created") not in data or len(data["model"])>2 or len(data["version"])>2: #????
            return JsonResponse({"message": "invalid data"}, status=400)
        
        try:
            created = datetime.strptime(data["created"],"%Y-%m-%d %H:%M:%S")
            if created > datetime.now():
                return JsonResponse({"message": "incorrect date"}, status=400) ## raise ValueError
            
        except ValueError:
            return JsonResponse({"message": "incorrect date"}, status=400)
        
        robot = Robot(serial=data["model"]+"-"+data["version"],model=data["model"],version=data["version"],created=created)
        robot.save()
        return JsonResponse({"message":"success"},status=200)