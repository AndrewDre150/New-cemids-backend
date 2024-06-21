from django.urls import path
# from .views import sensor_data1_view, latest_sensor_data_view, average_sensor_data_view, send_sms_view
from .views import *

urlpatterns = [
    path('data1/', sensor_data1_view, name='sensor-data1'),
    path('data1/latest/', latest_sensor_data_view, name='latest-sensor-data'),
    path('data1/average/', average_sensor_data_view, name='average-sensor-data'),
    path('data1/send-sms/', send_sms_view, name='send-sms'),
    path('data1/report/', co2_report_view, name='co2-report'),
]
