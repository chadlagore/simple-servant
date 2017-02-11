from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from traffic_api.models import *

@csrf_exempt
def receive_data(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        dataPackage = TrafficData()

        dataPackage.dataString = request.body
        pairs = request.body.decode().split('&')

        dataPackage.carCount = pairs[0].split('=')[1]
        dataPackage.latitude = pairs[1].split('=')[1]
        dataPackage.longitude = pairs[2].split('=')[1]
        dataPackage.timestamp = pairs[3].split('=')[1]
        dataPackage.save()
        return HttpResponse(status=200)
