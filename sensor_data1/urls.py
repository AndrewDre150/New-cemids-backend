from django.urls import path
# from .views import sensor_data1_view, latest_sensor_data_view, average_sensor_data_view, send_sms_view
from .views import *

urlpatterns = [
    path('data1/', sensor_data1_view, name='sensor-data1'),
    path('data1/latest/', latest_sensor_data_view, name='latest-sensor-data'),
    path('data1/average/', average_sensor_data_view, name='average-sensor-data'),
    path('data1/send-sms/', send_sms_view, name='send-sms'),
    path('data1/report/', co2_report_view, name='co2-report'),
    path('data1/first-70/', fetch_first_70_values, name='first-70-sensor-data'),
    path('data1/assign-daywise/', assign_daywise_values, name='assign-daywise-values'),
    path('data1/fetch-next-70/', fetch_next_70_values, name='fetch-next-70-values'),
    path('data1/assign-daywise2/', assign_daywise_values2, name='assign-daywise-values2'),
    
    path('data1/daily-values/', get_daily_co2_values, name='daily-co2-values'),
    path('data1/assign-weekly-averages/', get_weekly_average_co2, name='assign-weekly-averages'),
    
    path('data1/fetch-line-70/', fetch_line_70_values, name='fetch_line_70_values'),
    path('data1/assign-daywise3/', assign_daywise_values3, name='assign_daywise_values3'),
    
    path('data1/fetch-linegrapgh-70/', fetch_linegragh2_70_values, name='fetch_linegragh2_70_values'),
    path('data1/assign-daywise4/', assign_daywise_values4, name='assign-daywise-values4'),
    
]
