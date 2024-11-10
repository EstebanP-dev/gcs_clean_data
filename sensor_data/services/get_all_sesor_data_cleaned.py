
from django.http import JsonResponse

from ..models import SensorDataCleaned

def get_all_sesor_data_cleaned():
    try:
        data = SensorDataCleaned.objects.all().order_by('-timestamp')
        data_list = []
        for item in data:
            data_list.append({
                'timestamp': item.timestamp.isoformat(),
                'magnetometro': {
                    'x': item.mag_x,
                    'y': item.mag_y,
                    'z': item.mag_z
                },
                'barometro': item.barometro,
                'ruido': item.ruido,
                'giroscopio': {
                    'x': item.giro_x,
                    'y': item.giro_y,
                    'z': item.giro_z
                },
                'acelerometro': {
                    'x': item.acel_x,
                    'y': item.acel_y,
                    'z': item.acel_z
                },
                'vibracion': item.vibracion,
                'gps': {
                    'latitud': item.gps_lat,
                    'longitud': item.gps_lon
                }
            })
        return JsonResponse(data_list, safe=False)
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return JsonResponse({"error": "No se pudieron obtener los datos"}, status=500)