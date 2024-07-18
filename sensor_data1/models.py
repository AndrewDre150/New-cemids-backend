from django.db import models

class SensorData1(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    co2 = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - Temperature: {self.temperature}, CO2: {self.co2}"

