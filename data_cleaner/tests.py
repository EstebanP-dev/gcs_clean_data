from django.test import TestCase, Client
from django.urls import reverse
from .models import SensorData
import pandas as pd
import json

class DiagnosticDataCleanerTests(TestCase):
    def setUp(self):
        # Crear datos de prueba en la base de datos
        SensorData.objects.create(column1=1, column2='value1', column3=10.0)
        SensorData.objects.create(column1=2, column2='value2', column3=15.0)
        SensorData.objects.create(column1=1, column2='value1', column3=10.0)  # Duplicado
        SensorData.objects.create(column1=3, column2=None, column3=20.0)  # Valor faltante
        
        self.client = Client()
        self.clean_url = reverse('clean_diagnostic_data')

    def test_clean_diagnostic_data_success(self):
        # Preparar datos de prueba
        data = list(SensorData.objects.values())
        response = self.client.post(self.clean_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('cleaned_data', response_data)

    def test_clean_diagnostic_data_failure(self):
        # Forzar un error creando datos no válidos
        data = list(SensorData.objects.values())
        data.append({'column1': None, 'column2': None, 'column3': None})
        response = self.client.post(self.clean_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'failure')
        self.assertIn('errors', response_data)

    def test_cleaned_data_no_duplicates(self):
        data = list(SensorData.objects.values())
        response = self.client.post(self.clean_url, json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        cleaned_data = response_data.get('cleaned_data', [])
        df_cleaned = pd.DataFrame(cleaned_data)
        self.assertEqual(len(df_cleaned[df_cleaned.duplicated()]), 0)

    def test_cleaned_data_no_missing_values(self):
        data = list(SensorData.objects.values())
        response = self.client.post(self.clean_url, json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)
        cleaned_data = response_data.get('cleaned_data', [])
        df_cleaned = pd.DataFrame(cleaned_data)
        self.assertFalse(df_cleaned.isnull().values.any())