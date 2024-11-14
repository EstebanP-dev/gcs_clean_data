
from django.test import TestCase
from django.utils import timezone
from sensor_data.models import SensorData
from sensor_data.services.get_sensor_data_as_dataframe import get_sensor_data_as_dataframe


class GetSensorDataAsDataframeTests(TestCase):
    def setUp(self):
        SensorData.objects.create(
            mag_x=1.0,
            mag_y=2.0,
            mag_z=3.0,
            barometro=1013.25,
            ruido=45.5,
            giro_x=0.1,
            giro_y=0.2,
            giro_z=0.3,
            acel_x=0.01,
            acel_y=0.02,
            acel_z=0.03,
            vibracion=0.5,
            gps_lat=40.7128,
            gps_lon=-74.0060,
            timestamp=timezone.now()
        )

    def test_successful_data_retrieval(self):
        df = get_sensor_data_as_dataframe()
        self.assertFalse(df.empty)
        self.assertIn('mag_x', df.columns)