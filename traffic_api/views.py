from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from traffic_api.models import *
import datetime

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
        dataPackage.longitude = pairs[3].split('=')[1]
        timeStr = pairs[2].split('=')[1]

        hours = int(timeStr[0:2])
        minutes = int(timeStr[2:4])
        seconds = int(timeStr[4:6])

        time = datetime.time(hour=hours, minute=minutes, second=seconds)
        date = datetime.date.today()

        dataPackage.timestamp = datetime.datetime.combine(date, time)

        dataPackage.save()
        # print('Cars: ' + dataPackage.carCount)
        # print('Latitude: ' + dataPackage.latitude)
        # print('Longitude: ' + dataPackage.longitude)
        # print('Timestamp: ' + datetime.datetime.strftime(dataPackage.timestamp, "%d/%m/%y %H:%M:%S"))

        return HttpResponse(status=200)
