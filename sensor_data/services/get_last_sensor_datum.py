from django.http import JsonResponse

from ..models import SensorData

def get_last_sensor_datum():
    try:
        # Obtener el último registro
        latest_data = SensorData.objects.latest('timestamp')
        
        data = {
            'timestamp': latest_data.timestamp.isoformat(),
            'magnetometro': {
                'x': latest_data.mag_x,
                'y': latest_data.mag_y,
                'z': latest_data.mag_z
            },
            'barometro': latest_data.barometro,
            'ruido': latest_data.ruido,
            'giroscopio': {
                'x': latest_data.giro_x,
                'y': latest_data.giro_y,
                'z': latest_data.giro_z
            },
            'acelerometro': {
                'x': latest_data.acel_x,
                'y': latest_data.acel_y,
                'z': latest_data.acel_z
            },
            'vibracion': latest_data.vibracion,
            'gps': {
                'latitud': latest_data.gps_lat,
                'longitud': latest_data.gps_lon
            }
        }
        return JsonResponse(data, safe=False)
    except SensorData.DoesNotExist:
        return JsonResponse({"error": "No se encontraron datos"}, status=404)
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return JsonResponse({"error": "No se pudieron obtener los datos"}, status=500)
    