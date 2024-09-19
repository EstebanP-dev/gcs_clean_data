import pandas as pd
from typing import List, Dict
import json

from primitives import *
from src import Result, Success
from src.primitives.result import T


class DiagnosticDataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.expected_dtypes = {
            'id': 'object',
            'user_id': 'object',
            'timestamp': 'datetime64',
            'temperature': 'float64',
            'humidity': 'float64',
            'acceleration_x': 'float64',
            'acceleration_y': 'float64',
            'acceleration_z': 'float64',
            'vibration': 'float64',
            'sound_level': 'float64',
            'battery_level': 'float64',
            'magnetic_field_x': 'float64',
            'magnetic_field_y': 'float64',
            'magnetic_field_z': 'float64',
            'latitude': 'float64',
            'longitude': 'float64',
            'altitude': 'float64'
        }

    def validate_data_types(self) -> Result[Success]:
        errors = []
        for col, expected_type in self.expected_dtypes.items():
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                if actual_type != expected_type:
                    error_indices = self.df[~self.df[col].apply(lambda x: isinstance(x, eval(expected_type))).fillna(False)].index
                    for index in error_indices:
                        errors.append(Error.validation(f'Type mismatch in column {col} at row {index}. Expected: {expected_type}, Found: {actual_type}'))

        if errors:
            return Result.failure(errors)
        return Result.success()

    def validate_min_max(self) -> Result[Success]:
        errors = []
        limits = {
            'temperature': (-100, 100),
            'humidity': (0, 100),
            'acceleration_x': (-100, 100),
            'acceleration_y': (-100, 100),
            'acceleration_z': (-100, 100),
            'vibration': (0, 1000),
            'sound_level': (0, 200),
            'battery_level': (0, 100),
            'magnetic_field_x': (-1000, 1000),
            'magnetic_field_y': (-1000, 1000),
            'magnetic_field_z': (-1000, 1000),
            'latitude': (-90, 90),
            'longitude': (-180, 180),
            'altitude': (-500, 9000)
        }

        for col, (min_val, max_val) in limits.items():
            if col in self.df.columns:
                out_of_bounds = self.df[(self.df[col] < min_val) | (self.df[col] > max_val)]
                if not out_of_bounds.empty:
                    for idx in out_of_bounds.index:
                        errors.append(Error.validation(f'Value out of bounds in column {col} at row {idx}. Expected: [{min_val}, {max_val}], Found: {self.df[col].iloc[idx]}'))

        if errors:
            return Result.failure(errors)
        return Result.success()

    def check_missing_values(self) -> Result[Success]:
        errors = []
        for col in self.df.columns:
            null_rows = self.df[self.df[col].isnull()].index.tolist()
            for row in null_rows:
                errors.append(Error.validation(f'Missing value in column {col} at row {row}'))

        if errors:
            return Result.failure(errors)
        return Result.success()

    def check_duplicates(self) -> Result[Success]:
        errors = []
        duplicates = self.df[self.df.duplicated()]
        if not duplicates.empty:
            for idx in duplicates.index:
                errors.append(Error.validation(f'Duplicate row found at index {idx}'))

        if errors:
            return Result.failure(errors)
        return Result.success()

    def clean_data(self) -> pd.DataFrame:
        df_cleaned = self.df.drop_duplicates()
        df_cleaned = df_cleaned.apply(lambda x: x.fillna(x.mean()) if x.dtype in ['float64', 'int64'] else x)
        df_cleaned = df_cleaned.apply(lambda x: x.fillna('Missing') if x.dtype == 'object' else x)
        return df_cleaned

    def clean_and_validate_data(self, data: List[Dict]) -> Result[Success] | Result[T]:
        self.df = pd.DataFrame(data)

        result = self.validate_data_types()
        if result.is_failure:
            return result

        result = self.validate_min_max()
        if result.is_failure:
            return result

        result = self.check_missing_values()
        if result.is_failure:
            return result

        result = self.check_duplicates()
        if result.is_failure:
            return result

        df_cleaned = self.clean_data()

        cleaned_data = df_cleaned.to_dict(orient='records')

        return Result.success(cleaned_data)
