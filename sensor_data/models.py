# from django.db import models

# class SensorData(models.Model):
#     temperature = models.FloatField()
#     co2 = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# from django.db import models

# class SensorData(models.Model):
#     temperature = models.FloatField()
#     co2 = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Temperature: {self.temperature}, CO2: {self.co2}'

from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    co2 = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Temperature: {self.temperature}, CO2: {self.co2}'
