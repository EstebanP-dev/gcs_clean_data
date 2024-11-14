from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, MagicMock
from datetime import datetime
from sensor_data.services.insert_clean_data import insert_clean_data
from sensor_data.models import SensorDataCleaned


class InsertCleanDataTests(TestCase):
    def setUp(self):
        self.test_data = {
            'sensor1': 10.5,
            'sensor2': 20.3
        }
        self.gps_mock_data = {
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        self.valid_data = {
            'mag_x': 1.0,
            'mag_y': 2.0,
            'mag_z': 3.0,
            'barometro': 1013.25,
            'ruido': 45.5,
            'giro_x': 0.1,
            'giro_y': 0.2,
            'giro_z': 0.3,
            'acel_x': 0.01,
            'acel_y': 0.02,
            'acel_z': 0.03,
            'vibracion': 0.5,
            'gps_lat': 40.7128,
            'gps_lon': -74.0060,
            'timestamp': timezone.now(),
            'outlier_score': 1.5
        }

    @patch('sensor_data.utils.GPS')
    def test_successful_insert(self, mock_gps):
        # Configure GPS mock
        mock_gps_instance = MagicMock()
        mock_gps_instance.get_position.return_value = self.gps_mock_data
        mock_gps.return_value = mock_gps_instance

        # Execute function
        result = insert_clean_data(self.test_data)

        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result['gps_lat'], self.gps_mock_data['latitude'])
        self.assertEqual(result['gps_lon'], self.gps_mock_data['longitude'])
        self.assertIn('timestamp', result)

        # Verify database entry
        saved_data = SensorDataCleaned.objects.first()
        self.assertIsNotNone(saved_data)
        self.assertEqual(saved_data.sensor1, self.test_data['sensor1'])
        self.assertEqual(saved_data.sensor2, self.test_data['sensor2'])

    @patch('sensor_data.utils.GPS')
    def test_gps_failure(self, mock_gps):
        # Configure GPS mock to raise exception
        mock_gps_instance = MagicMock()
        mock_gps_instance.get_position.side_effect = Exception("GPS Error")
        mock_gps.return_value = mock_gps_instance

        # Execute function
        result = insert_clean_data(self.test_data)

        # Verify result
        self.assertIsNone(result)
        self.assertEqual(SensorDataCleaned.objects.count(), 0)

    @patch('sensor_data.models.SensorDataCleaned.objects.create')
    def test_database_error(self, mock_create):
        # Simulate database error
        mock_create.side_effect = Exception("Database error")
        result = insert_clean_data(self.valid_data)
        self.assertIsNone(result)

    @patch('sensor_data.utils.GPS')
    def test_timestamp_creation(self, mock_gps):
        # Configure GPS mock if needed
        mock_gps_instance = MagicMock()
        mock_gps.return_value = mock_gps_instance

        result = insert_clean_data(self.valid_data)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.timestamp)