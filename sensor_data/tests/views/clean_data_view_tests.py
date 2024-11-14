from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch, MagicMock
import pandas as pd

from shared_kernel import BaseTestCase
from sensor_data.models import SensorData

class CleanDataViewTests(BaseTestCase):
    def setUp(self):
        self.client = Client()
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        # Create regular user
        self.user = User.objects.create_user(
            username='user',
            password='user123'
        )
        self.client.login(username='testuser', password='testpass')
        # Create sample data
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
        SensorData.objects.create(
            mag_x=1.1,
            mag_y=2.1,
            mag_z=3.1,
            barometro=1013.26,
            ruido=45.6,
            giro_x=0.2,
            giro_y=0.3,
            giro_z=0.4,
            acel_x=0.02,
            acel_y=0.03,
            acel_z=0.04,
            vibracion=0.6,
            gps_lat=40.7129,
            gps_lon=-74.0061,
            timestamp=timezone.now()
        )

    def test_unauthorized_access(self):
        # Login as regular user
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('sensor_data:clean_data'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'error': 'Unauthorized'})

    @patch('sensor_data.services.get_sensor_data_as_dataframe')
    def test_no_data_available(self, mock_get_data):
        mock_get_data.return_value = None
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('sensor_data:clean_data'))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'No se pudieron obtener los datos para limpiar'})

    @patch('sensor_data.services.get_sensor_data_as_dataframe')
    @patch('sensor_data.services.DiagnosticDataCleaner')
    def test_validation_failure(self, mock_cleaner, mock_get_data):
        # Mock DataFrame
        mock_df = pd.DataFrame({
            'numeric1': [1.0, 2.0, 3.0],
            'numeric2': [4.0, 5.0, 6.0]
        })
        mock_get_data.return_value = mock_df
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('sensor_data:clean_data'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'errors': ['Error 1']})

    @patch('sensor_data.services.get_sensor_data_as_dataframe')
    @patch('sensor_data.services.DiagnosticDataCleaner')
    @patch('sensor_data.services.insert_clean_data')
    def test_insert_data_failure(self, mock_insert, mock_cleaner, mock_get_data):
        # Mock DataFrame
        mock_df = pd.DataFrame()
        mock_get_data.return_value = mock_df
        
        # Mock cleaner
        mock_cleaner_instance = MagicMock()
        mock_cleaner_instance.clean_and_validate_data.return_value.is_failure = False
        mock_cleaner_instance.clean_and_validate_data.return_value.value = [{'data': 'test'}]
        mock_cleaner.return_value = mock_cleaner_instance

        # Mock insert failure
        mock_insert.return_value = None

        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('sensor_data:clean_data'))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'message': 'Something went wrong!'})

    @patch('sensor_data.services.get_sensor_data_as_dataframe')
    @patch('sensor_data.services.DiagnosticDataCleaner')
    @patch('sensor_data.services.insert_clean_data')
    def test_successful_cleaning(self, mock_insert, mock_cleaner, mock_get_data):
        # Mock DataFrame
        mock_df = pd.DataFrame()
        mock_get_data.return_value = mock_df
        
        # Mock cleaner
        mock_cleaner_instance = MagicMock()
        mock_cleaner_instance.clean_and_validate_data.return_value.is_failure = False
        mock_cleaner_instance.clean_and_validate_data.return_value.value = [{'data': 'test'}]
        mock_cleaner.return_value = mock_cleaner_instance

        # Mock successful insert
        mock_insert.return_value = True

        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('sensor_data:clean_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Data cleaned successfully'})