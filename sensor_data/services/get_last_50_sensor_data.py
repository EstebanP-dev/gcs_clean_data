from django.http import JsonResponse
from ..models import SensorData
from statistics import mean, median, stdev

def calculate_statistics(values):
    if not values:
        return None
    
    sorted_values = sorted(values)
    n = len(sorted_values)

    def percentile(p):
        if n == 0:
            return None
        if p == 0:
            return sorted_values[0]
        if p == 100:
            return sorted_values[-1]
        i = int(((n - 1) * p) / 100)
        return sorted_values[i]
    
    try:
        return {
            'mean': mean(values),
            'std_dev': stdev(values) if n > 1 else 0,
            'q1': percentile(25),
            'median': median(values),
            'q3': percentile(75),
            'p90': percentile(90),
            'p95': percentile(95)
        }
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return None

def get_last_50_sensor_data():
    try:
        # Obtener los últimos 50 registros ordenados
        data = list(SensorData.objects.order_by('-id')[:50].values(
            'id', 'mag_x', 'mag_y', 'mag_z', 'barometro', 'ruido',
            'giro_x', 'giro_y', 'giro_z', 'acel_x', 'acel_y', 'acel_z',
            'vibracion', 'gps_lat', 'gps_lon'
        ))[::-1]  # Invertir el orden para obtener en orden cronológico

        avg_data = {'id': 'latest_50'}
        stats_data = {'id': 'latest_50'}

        # Lista de campos del sensor para calcular estadísticas
        sensor_fields = [
            'mag_x', 'mag_y', 'mag_z', 'barometro', 'ruido',
            'giro_x', 'giro_y', 'giro_z', 'acel_x', 'acel_y', 'acel_z',
            'vibracion', 'gps_lat', 'gps_lon'
        ]

        # Calcular promedios y estadísticas para cada campo
        for field in sensor_fields:
            field_values = [item[field] for item in data]

            # Calcular media
            avg_data[field] = sum(field_values) / len(field_values)

            # Calcular estadísticas
            stats_data[f"{field}_stats"] = calculate_statistics(field_values)

        # Construir el JSON final
        grouped_data = [{
            'averages': avg_data,
            'statistics': stats_data
        }]

        return JsonResponse(grouped_data, safe=False)
    except SensorData.DoesNotExist:
        return JsonResponse({"error": "No se encontraron datos"}, status=404)
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return JsonResponse({"error": "No se pudieron obtener los datos"}, status=500)