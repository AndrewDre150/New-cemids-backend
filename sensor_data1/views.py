
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


# def get_co2_data(request):
#     # Fetch all sensor data
#     sensor_data = SensorData1.objects.all()

#     # Initialize a dictionary to hold CO2 levels for each day of the week
#     days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#     co2_levels = {day: None for day in days}

#     # Populate the dictionary with CO2 values
#     for data in sensor_data:
#         day_of_week = data.timestamp.strftime("%a")
#         if co2_levels[day_of_week] is None:
#             co2_levels[day_of_week] = data.co2
#         else:
#             co2_levels[day_of_week] = max(co2_levels[day_of_week], data.co2)

#     # Convert to list of dictionaries for the frontend
#     co2_data = [{"day": day, "Co2_level": co2_levels[day] or 0} for day in days]

#     return JsonResponse(co2_data, safe=False)




def fetch_first_70_values(request):
    # Fetch first 70 sensor data entries
    first_70_data = SensorData1.objects.order_by('timestamp')[:70]

    # Prepare a response with the fetched data (for demonstration purposes)
    response_data = "\n".join([str(data) for data in first_70_data])

    return HttpResponse(response_data)



def assign_daywise_values(request):
    # Fetch first 70 sensor data entries
    first_70_data = SensorData1.objects.order_by('timestamp')[:70]

    # Initialize day-wise CO2 data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_values = {day: [] for day in days}

    # Assign CO2 levels to respective days
    for idx, data in enumerate(first_70_data):
        day_index = idx % 7  # Calculate the day index (0 for Mon, 1 for Tue, ..., 6 for Sun)
        day = days[day_index]
        day_values[day].append(data.co2)  # Ensure 'co2' matches your model field name

    # Calculate average CO2 levels for each day
    average_co2_levels = []
    for day in days:
        values_for_day = day_values[day][:10]  # Get the first 10 values for the current day
        if values_for_day:  # Check if there are values for the day
            average_co2_level = sum(values_for_day) / len(values_for_day)
        else:
            average_co2_level = 0  # Default to 0 if no values

        average_co2_levels.append({"day": day, "average_co2": round(average_co2_level, 2)})

    # Return the result as JSON array
    return JsonResponse(average_co2_levels, safe=False)







def fetch_next_70_values(request):
    # Fetch next 70 sensor data entries (starting from the 71st entry)
    next_70_data = SensorData1.objects.order_by('timestamp')[70:140]

    # Prepare a response with the fetched data
    response_data = [
        {"timestamp": data.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "co2": data.co2}
        for data in next_70_data
    ]

    return JsonResponse(response_data, safe=False)



def assign_daywise_values2(request):
    # Fetch next 70 sensor data entries
    next_70_data = SensorData1.objects.order_by('timestamp')[70:140]

    # Initialize day-wise CO2 data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_values = {day: [] for day in days}

    # Assign CO2 levels to respective days
    for idx, data in enumerate(next_70_data):
        day_index = idx % 7  # Calculate the day index (0 for Mon, 1 for Tue, ..., 6 for Sun)
        day = days[day_index]
        day_values[day].append(data.co2)  # Ensure 'co2' matches your model field name

    # Calculate average CO2 levels for each day
    average_co2_levels = []
    for day in days:
        values_for_day = day_values[day]
        if values_for_day:  # Check if there are values for the day
            average_co2_level = sum(values_for_day) / len(values_for_day)
        else:
            average_co2_level = 0  # Default to 0 if no values

        average_co2_levels.append({"day": day, "average_co2": round(average_co2_level, 2)})

    # Return the result as JSON array
    return JsonResponse(average_co2_levels, safe=False)