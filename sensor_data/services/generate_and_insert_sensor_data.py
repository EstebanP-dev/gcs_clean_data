import datetime
import random

from ..models import SensorData
from ..utils import GPS

gps_instance = GPS()

def generate_and_insert_sensor_data():
    current_time = datetime.datetime.now()
    gps_data = gps_instance.get_position(use_current_location=False)
    
    new_data = {
        'timestamp': current_time,
        'mag_x': random.uniform(-100, 100),
        'mag_y': random.uniform(-100, 100),
        'mag_z': random.uniform(-100, 100),
        'barometro': random.uniform(900, 1100),
        'ruido': random.uniform(30, 120),
        'giro_x': random.uniform(-180, 180),
        'giro_y': random.uniform(-180, 180),
        'giro_z': random.uniform(-180, 180),
        'acel_x': random.uniform(-10, 10),
        'acel_y': random.uniform(-10, 10),
        'acel_z': random.uniform(-10, 10),
        'vibracion': random.uniform(0, 10),
        'gps_lat': gps_data['latitude'],
        'gps_lon': gps_data['longitude'],
    }
    sensor_data = SensorData(**new_data)
    sensor_data.save()
    
    # Opcional: Limitar el número de registros a los últimos 100
    # total_records = SensorData.objects.count()
    # if total_records > 100:
    #     records_to_delete = total_records - 100
    #     SensorData.objects.all().order_by('timestamp')[:records_to_delete].delete()