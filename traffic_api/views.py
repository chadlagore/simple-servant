from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def receive_data(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse(status=200)
