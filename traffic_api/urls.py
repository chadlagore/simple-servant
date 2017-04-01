from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^data', views.receive_data, name='receive_data'),
    url(r'^intersections', views.all_intersection_activity,
        name='all_intersection_activity'),
    url(r'^historical', views.historical_request,
        name='historical_request')
]
