from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^data', views.receive_data, name='receive_data'),
]