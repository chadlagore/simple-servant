from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from traffic_api.models import *
import datetime

@csrf_exempt
def receive_data(request):
    if request.method == 'GET':
        data = TrafficData.objects.all()
        # datum1 = {}
        # datum1['carCount'] = 24
        # datum1['latitude'] = 14.5266
        # datum1['longitude'] = 128.5257
        # datum1['timestamp'] = datetime.datetime.utcnow()
        #
        # datum2 = {}
        # datum2['carCount'] = 12
        # datum2['latitude'] = 14.7378
        # datum2['longitude'] = 128.4572
        # datum2['timestamp'] = datetime.datetime.utcnow()

        return render(request, 'index.html', {'data': data})
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

        return HttpResponse(status=200)
