# from django.shortcuts import render

# from django.db.models import Avg
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import SensorData1
# from .serializers import SensorData1Serializer
# from django.http import JsonResponse

# from django.http import HttpResponse
# from twilio.rest import Client
# from .twilio_credentials import account_sid, auth_token, twilio_from_number

# from django.db.models import Avg, Max, Min, Sum, StdDev, Count, Q
# from django.http import JsonResponse


# @api_view(['POST'])
# def sensor_data1_view(request):
#     if request.method == 'POST':
#         serializer = SensorData1Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)  # Return serialized data if saved successfully
#         return Response(serializer.errors, status=400)  # Return validation errors if data is not valid
#     else:
#         return Response({'detail': 'Method "GET" not allowed.'}, status=405)


# def latest_sensor_data_view(request):
#     try:
#         latest_data = SensorData1.objects.latest('timestamp')  # Get the latest data based on timestamp
#         serializer = SensorData1Serializer(latest_data)
#         return JsonResponse(serializer.data)
#     except SensorData1.DoesNotExist:
#         return JsonResponse({"error": "No data available"}, status=404)
    

# def average_sensor_data_view(request):
#     try:
#         last_10_values = SensorData1.objects.order_by('-timestamp')[:10]
#         average_co2 = last_10_values.aggregate(avg_co2=Avg('co2'))['avg_co2'] or 0
#         return JsonResponse({'average_co2': average_co2})
#     except SensorData1.DoesNotExist:
#         return JsonResponse({"error": "No data available"}, status=404)
    

# def send_sms_view(request):
#     # Get the average CO2 reading from the last 10 values
#     last_10_values = SensorData1.objects.order_by('-timestamp')[:10]
#     average_co2 = last_10_values.aggregate(avg_co2=Avg('co2'))['avg_co2'] or 0

#     # Set the threshold value (e.g., 800)
#     threshold = 600

#     # Check if CO2 level exceeds the threshold
#     if average_co2 > threshold:
#         # Send SMS using Twilio
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#             from_=twilio_from_number,
#             body=f"""Alert: Average CO2 level exceeded {threshold} ppm! 
#                     Current average level: {average_co2} ppm. 
#                     Please take immediate action to reduce emissions and ensure a safe environment.""",
#             to='+256700294565'  # Replace with your phone number
#             # to='+256708187424'  
#         )
#         return HttpResponse('SMS sent successfully!')
#     else:
#         return HttpResponse('CO2 level is within safe limits.')
    
# # @api_view(['GET'])

# def co2_report_view(request):
#     total_co2 = SensorData1.objects.aggregate(total_co2=Sum('co2'))['total_co2']
#     avg_daily_co2 = SensorData1.objects.values('timestamp__date').annotate(daily_avg=Avg('co2')).aggregate(avg_daily_co2=Avg('daily_avg'))['avg_daily_co2']
#     max_co2 = SensorData1.objects.aggregate(max_co2=Max('co2'))['max_co2']
#     # min_co2 = SensorData1.objects.aggregate(min_co2=Min('co2'))['min_co2']
#     # min_co2 = SensorData1.objects.filter(co2__gt=0).aggregate(min_co2=Min('co2'))['min_co2']
#     min_co2 = SensorData1.objects.filter(co2__gt=0).filter(co2__gt=100).aggregate(min_co2=Min('co2'))['min_co2']
#     co2_range = max_co2 - min_co2
#     common_co2 = SensorData1.objects.values('co2').annotate(count=Count('co2')).order_by('-count').first()['co2']
#     low_co2_days = SensorData1.objects.values('timestamp__date').annotate(daily_min=Min('co2')).filter(daily_min__lt=400).count()
#     high_co2_days = SensorData1.objects.values('timestamp__date').annotate(daily_max=Max('co2')).filter(daily_max__gt=1000).count()
#     std_dev_co2 = SensorData1.objects.aggregate(std_dev_co2=StdDev('co2'))['std_dev_co2']
#     high_readings_count = SensorData1.objects.filter(co2__gt=2000).count()

#     weather_conditions = "Clear"  # Placeholder value, update with actual data if available
#     sensor_model = "MH-Z19"  # Placeholder value, update with actual data if available

#     report_data = {
#         'total_co2': total_co2,
#         # 'avg_daily_co2': avg_daily_co2,
#         'avg_daily_co2': round(avg_daily_co2, 2),
#         'max_co2': max_co2,
#         'min_co2': min_co2,
#         'co2_range': co2_range,
#         'common_co2': common_co2,
#         'low_co2_days': low_co2_days,
#         'high_co2_days': high_co2_days,
#         # 'std_dev_co2': std_dev_co2,
#         'std_dev_co2': round(std_dev_co2, 2), 
#         'weather_conditions': weather_conditions,
#         'sensor_model': sensor_model,
#         'high_readings_count': high_readings_count,
#     }
#     return JsonResponse(report_data)


from django.shortcuts import render
from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData1
from .serializers import SensorData1Serializer
from django.http import JsonResponse, HttpResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Twilio credentials from environment variables
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
twilio_from_number = os.getenv('TWILIO_FROM_NUMBER')

from django.db.models import Avg, Max, Min, Sum, StdDev, Count, Q

@api_view(['POST'])
def sensor_data1_view(request):
    if request.method == 'POST':
        serializer = SensorData1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return serialized data if saved successfully
        return Response(serializer.errors, status=400)  # Return validation errors if data is not valid
    else:
        return Response({'detail': 'Method "GET" not allowed.'}, status=405)

def latest_sensor_data_view(request):
    try:
        latest_data = SensorData1.objects.latest('timestamp')  # Get the latest data based on timestamp
        serializer = SensorData1Serializer(latest_data)
        return JsonResponse(serializer.data)
    except SensorData1.DoesNotExist:
        return JsonResponse({"error": "No data available"}, status=404)

def average_sensor_data_view(request):
    try:
        last_10_values = SensorData1.objects.order_by('-timestamp')[:10]
        average_co2 = last_10_values.aggregate(avg_co2=Avg('co2'))['avg_co2'] or 0
        return JsonResponse({'average_co2': average_co2})
    except SensorData1.DoesNotExist:
        return JsonResponse({"error": "No data available"}, status=404)

def send_sms_view(request):
    # Get the average CO2 reading from the last 10 values
    last_10_values = SensorData1.objects.order_by('-timestamp')[:10]
    average_co2 = last_10_values.aggregate(avg_co2=Avg('co2'))['avg_co2'] or 0

    # Set the threshold value (e.g., 800)
    threshold = 600

    # Check if CO2 level exceeds the threshold
    if average_co2 > threshold:
        # Send SMS using Twilio
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=twilio_from_number,
            body=f"""Alert: Average CO2 level exceeded {threshold} ppm! 
                    Current average level: {average_co2} ppm. 
                    Please take immediate action to reduce emissions and ensure a safe environment.""",
            to='+256700294565'  # Replace with your phone number
        )
        return HttpResponse('SMS sent successfully!')
    else:
        return HttpResponse('CO2 level is within safe limits.')

def co2_report_view(request):
    total_co2 = SensorData1.objects.aggregate(total_co2=Sum('co2'))['total_co2']
    avg_daily_co2 = SensorData1.objects.values('timestamp__date').annotate(daily_avg=Avg('co2')).aggregate(avg_daily_co2=Avg('daily_avg'))['avg_daily_co2']
    max_co2 = SensorData1.objects.aggregate(max_co2=Max('co2'))['max_co2']
    min_co2 = SensorData1.objects.filter(co2__gt=0).filter(co2__gt=100).aggregate(min_co2=Min('co2'))['min_co2']
    co2_range = max_co2 - min_co2
    common_co2 = SensorData1.objects.values('co2').annotate(count=Count('co2')).order_by('-count').first()['co2']
    low_co2_days = SensorData1.objects.values('timestamp__date').annotate(daily_min=Min('co2')).filter(daily_min__lt=400).count()
    high_co2_days = SensorData1.objects.values('timestamp__date').annotate(daily_max=Max('co2')).filter(daily_max__gt=1000).count()
    std_dev_co2 = SensorData1.objects.aggregate(std_dev_co2=StdDev('co2'))['std_dev_co2']
    high_readings_count = SensorData1.objects.filter(co2__gt=2000).count()

    weather_conditions = "Clear"  # Placeholder value, update with actual data if available
    sensor_model = "MH-Z19"  # Placeholder value, update with actual data if available

    report_data = {
        'total_co2': total_co2,
        'avg_daily_co2': round(avg_daily_co2, 2),
        'max_co2': max_co2,
        'min_co2': min_co2,
        'co2_range': co2_range,
        'common_co2': common_co2,
        'low_co2_days': low_co2_days,
        'high_co2_days': high_co2_days,
        'std_dev_co2': round(std_dev_co2, 2),
        'weather_conditions': weather_conditions,
        'sensor_model': sensor_model,
        'high_readings_count': high_readings_count,
    }
    return JsonResponse(report_data)
