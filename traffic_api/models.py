from django.db import models


class TrafficData(models.Model):
    dataString = models.CharField(max_length=1024)
    carCount = models.IntegerField(null=True)
    timestamp = models.DateTimeField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


class IntersectionData(models.Model):
    id = models.BigIntegerField(null=False, primary_key=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    street_a = models.CharField(max_length=1024, null=True)
    street_b = models.CharField(max_length=1024, null=True)

    def as_json(self):
        return dict(
            id=self.id,
            latitude=self.latitude,
            longitude=self.longitude,
            street_a=self.street_a,
            street_b=self.street_b)

    class Meta:
        unique_together = ('latitude', 'longitude')
