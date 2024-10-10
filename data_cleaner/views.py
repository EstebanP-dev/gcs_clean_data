import json
from django.shortcuts import render
from models import SensorData 
from django.http import JsonResponse
from .services.diagnostic_data_cleaner import SensorDataCleaner

def say_hello(request):
    return render(request, 'hello.html')

def clean_data_view(request):
    if request.method == 'POST':
        try:
            input_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if input_data:
            try:
                cleaner = SensorDataCleaner(input_data)
                cleaned_data = cleaner.clean_and_validate_data()
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No data provided'}, status=400)

        return JsonResponse({'cleaned_data': cleaned_data}, status=200)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
