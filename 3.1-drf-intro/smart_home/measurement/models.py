from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(null=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
