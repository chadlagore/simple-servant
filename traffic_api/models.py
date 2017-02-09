from django.db import models

class TrafficData(models.Model):
    data = models.CharField(max_length=1024)
