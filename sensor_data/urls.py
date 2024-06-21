from django.urls import path
from sensor_data import views

urlpatterns = [
    path('data', views.save_sensor_data, name='save_sensor_data'),
  
]