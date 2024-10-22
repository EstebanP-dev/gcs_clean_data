import pandas as pd

from ..models import SensorData

def get_sensor_data_as_dataframe():
    try:
        data = SensorData.objects.all().values(
            'timestamp', 'mag_x', 'mag_y', 'mag_z', 'barometro', 'ruido',
            'giro_x', 'giro_y', 'giro_z', 'acel_x', 'acel_y', 'acel_z',
            'vibracion', 'gps_lat', 'gps_lon'
        )
        df = pd.DataFrame(list(data))
        return df
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return None  # o maneja la excepción según sea necesario