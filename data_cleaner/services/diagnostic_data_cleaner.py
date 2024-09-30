import pandas as pd
import numpy as np
from scipy.spatial.distance import mahalanobis

from ..primitives.result import Result
from ..primitives.error import Error
from ..primitives.units import Success

class DiagnosticDataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def calculate_mahalanobis(self, df: pd.DataFrame) -> np.ndarray:
        numeric_cols = df.select_dtypes(include=['float64', 'int64'])
        cov_matrix = np.cov(numeric_cols.values, rowvar=False)
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        mean_vals = np.mean(numeric_cols, axis=0)
        mahalanobis_distances = np.apply_along_axis(lambda x: mahalanobis(x, mean_vals, inv_cov_matrix), 1, numeric_cols)
        return mahalanobis_distances

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

        df_cleaned = df_cleaned.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.dtype in ['object'] else col)

        df_cleaned = df_cleaned.apply(lambda x: x.fillna(x.mean()) if x.dtype in ['float64', 'int64'] else x)
        df_cleaned = df_cleaned.apply(lambda x: x.fillna('Missing') if x.dtype == 'object' else x)

        mahalanobis_distances = self.calculate_mahalanobis(df_cleaned)
        threshold = np.percentile(mahalanobis_distances, 95)

        df_cleaned = df_cleaned[mahalanobis_distances <= threshold]

        return df_cleaned
    

    def clean_and_validate_data(self):
        df_cleaned = self.clean_data()

        df = df_cleaned
        result = self.check_missing_values()
        if result.is_failure:
            return result

        result = self.check_duplicates()
        if result.is_failure:
            return result

        cleaned_data = df_cleaned.to_dict(orient='records')

        return Result.success(cleaned_data)
