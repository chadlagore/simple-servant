from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def receive_data(request):
    return HttpResponse(status=200)