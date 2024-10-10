import pandas as pd
import numpy as np
from scipy.spatial.distance import mahalanobis

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from models import SensorData  

class SensorDataCleaner(View):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_mahalanobis(self, df: pd.DataFrame) -> np.ndarray:
        numeric_cols = df.select_dtypes(include=['float64', 'int64'])
        cov_matrix = np.cov(numeric_cols.values, rowvar=False)
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        mean_vals = np.mean(numeric_cols, axis=0)
        mahalanobis_distances = np.apply_along_axis(lambda x: mahalanobis(x, mean_vals, inv_cov_matrix), 1, numeric_cols)
        return mahalanobis_distances

    def check_missing_values(self):
        errors = []
        for col in self.df.columns:
            null_rows = self.df[self.df[col].isnull()].index.tolist()
            for row in null_rows:
                errors.append(f'Missing value in column {col} at row {row}')

        if errors:
            raise ValidationError(errors)

    def check_duplicates(self):
        errors = []
        duplicates = self.df[self.df.duplicated()]
        if not duplicates.empty:
            for idx in duplicates.index:
                errors.append(f'Duplicate row found at index {idx}')

        if errors:
            raise ValidationError(errors)

    def clean_data(self) -> pd.DataFrame:
        df_cleaned = self.df.drop_duplicates()

        df_cleaned = df_cleaned.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.dtype in ['object'] else col)

        df_cleaned = df_cleaned.apply(lambda x: x.fillna(x.mean()) if x.dtype in ['float64', 'int64'] else x)
        df_cleaned = df_cleaned.apply(lambda x: x.fillna('Missing') if x.dtype == 'object' else x)

        mahalanobis_distances = self.calculate_mahalanobis(df_cleaned)
        threshold = np.percentile(mahalanobis_distances, 95)

        df_cleaned = df_cleaned[mahalanobis_distances <= threshold]

        return df_cleaned

    def clean_and_validate_data(self):
        df_cleaned = self.clean_data()

        self.df = df_cleaned
        self.check_missing_values()
        self.check_duplicates()

        cleaned_data = df_cleaned.to_dict(orient='records')

        return cleaned_data

class CleanSensorDataView(View):
    def get(self, request, *args, **kwargs):
        data = list(SensorData.objects.values())
        df = pd.DataFrame(data)

        cleaner = SensorDataCleaner(df)
        try:
            cleaned_data = cleaner.clean_and_validate_data()
        except ValidationError as e:
            return JsonResponse({'status': 'failure', 'errors': e.messages}, status=400)

        return JsonResponse({'status': 'success', 'cleaned_data': cleaned_data}, status=200)

