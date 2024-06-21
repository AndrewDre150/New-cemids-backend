

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt  # Temporary to allow POST requests without CSRF token in development
# def sensor_data_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             temperature = data.get('temperature')
#             co2 = data.get('co2')
            
#             # Example: Save data to a model
#             # Assuming you have a SensorData model in models.py
#             from .models import SensorData
#             SensorData.objects.create(temperature=temperature, co2=co2)
            
#             return JsonResponse({'message': 'Data received successfully'}, status=200)
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'POST request required only'}, status=400)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import SensorData

# @csrf_exempt
# def save_sensor_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             temperature = data.get('temperature')
#             co2 = data.get('co2')
            
#             # Save data to a model
#             SensorData.objects.create(temperature=temperature, co2=co2)
            
#             return JsonResponse({'message': 'Data received successfully'}, status=200)
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'POST request required'}, status=405)

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import SensorData

# @csrf_exempt
# def save_sensor_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             temperature = data.get('temperature')
#             co2 = data.get('co2')
            
#             # Save data to a model
#             SensorData.objects.create(temperature=temperature, co2=co2)
            
#             return JsonResponse({'message': 'Data received successfully'}, status=200)
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'POST request required'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData

@csrf_exempt  # Temporary to allow POST requests without CSRF token in development
def save_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            co2 = data.get('co2')
            
            # Example: Save data to a model
            SensorData.objects.create(temperature=temperature, co2=co2)
            
            return JsonResponse({'message': 'Data received successfully'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'GET':
        # Example: Retrieve data from a model
        sensor_data = list(SensorData.objects.all().values())
        return JsonResponse(sensor_data, safe=False)
    
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
