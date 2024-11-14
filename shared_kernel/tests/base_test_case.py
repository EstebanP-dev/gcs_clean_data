from django.test import TransactionTestCase
from django.utils import timezone
from django.core.management import call_command

import pandas as pd

from sensor_data.models import SensorData


class BaseTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('migrate', verbosity=0, interactive=False)

    def setUp(self):
        super().setUp()
        self.create_test_data()

    def create_test_data(self):
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