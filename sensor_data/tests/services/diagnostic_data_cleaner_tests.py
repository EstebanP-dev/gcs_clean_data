import pytest
import pandas as pd
import numpy as np

from ...services.diagnostic_data_cleaner import DiagnosticDataCleaner

class DiagnosticDataCleanerTests:
    @pytest.fixture
    def valid_df(self):
        """Fixture para un DataFrame válido"""
        return pd.DataFrame({
            'numeric1': [1.0, 2.0, 3.0, 4.0, 5.0],
            'numeric2': [2.0, 4.0, 6.0, 8.0, 10.0],
            'string_col': ['1', '2', '3', '4', '5'],
            'high_null': [1.0, None, None, None, None],
            'constant': [1.0, 1.0, 1.0, 1.0, 1.0]
        })

    @pytest.fixture
    def numeric_df(self):
        """Fixture para un DataFrame solo numérico"""
        return pd.DataFrame({
            'numeric1': [1.0, 2.0, 3.0],
            'numeric2': [2.0, 4.0, 6.0]
        })

    def test_init(self, valid_df):
        """Test de inicialización"""
        cleaner = DiagnosticDataCleaner(valid_df)
        assert isinstance(cleaner.df, pd.DataFrame)
        assert cleaner.df.equals(valid_df)

    def test_calculate_mahalanobis_valid_data(self, numeric_df):
        """Test del cálculo de distancia Mahalanobis con datos válidos"""
        cleaner = DiagnosticDataCleaner(numeric_df)
        distances = cleaner.calculate_mahalanobis(numeric_df)
        assert isinstance(distances, np.ndarray)
        assert len(distances) == len(numeric_df)
        assert not np.isnan(distances).any()

    def test_calculate_mahalanobis_with_nans(self):
        """Test del cálculo de Mahalanobis con NaNs"""
        df_with_nans = pd.DataFrame({
            'numeric1': [1.0, np.nan, 3.0],
            'numeric2': [2.0, 4.0, 6.0]
        })
        cleaner = DiagnosticDataCleaner(df_with_nans)
        with pytest.raises(ValueError, match="Existen valores NaN"):
            cleaner.calculate_mahalanobis(df_with_nans)

    def test_calculate_mahalanobis_singular_matrix(self):
        """Test del cálculo de Mahalanobis con matriz singular"""
        singular_df = pd.DataFrame({
            'numeric1': [1.0, 2.0, 3.0],
            'numeric2': [2.0, 4.0, 6.0],  # perfectamente correlacionada con numeric1
        })
        cleaner = DiagnosticDataCleaner(singular_df)
        with pytest.raises(ValueError, match="La matriz de covarianza es singular"):
            cleaner.calculate_mahalanobis(singular_df)

    def test_clean_data_basic(self, valid_df):
        """Test básico de limpieza de datos"""
        cleaner = DiagnosticDataCleaner(valid_df)
        cleaned_df = cleaner.clean_data()
        
        assert isinstance(cleaned_df, pd.DataFrame)
        assert 'high_null' not in cleaned_df.columns  # columna con muchos nulos debe ser eliminada
        assert 'constant' not in cleaned_df.columns  # columna constante debe ser eliminada
        assert not cleaned_df.isnull().values.any()  # no debe haber NaNs

    def test_clean_data_string_conversion(self, valid_df):
        """Test de conversión de strings a números"""
        cleaner = DiagnosticDataCleaner(valid_df)
        cleaned_df = cleaner.clean_data()
        assert cleaned_df['string_col'].dtype in ['float64', 'int64']

    def test_clean_and_validate_data(self, valid_df):
        """Test del proceso completo de limpieza y validación"""
        cleaner = DiagnosticDataCleaner(valid_df)
        result = cleaner.clean_and_validate_data()
        
        assert result.is_success
        assert isinstance(result.value, list)
        assert len(result.value) > 0
        assert isinstance(result.value[0], dict)

    def test_clean_data_insufficient_rows(self):
        """Test con DataFrame de una sola fila"""
        single_row_df = pd.DataFrame({
            'numeric1': [1.0],
            'numeric2': [2.0]
        })
        cleaner = DiagnosticDataCleaner(single_row_df)
        with pytest.raises(ValueError, match="Se requieren al menos dos filas"):
            cleaner.clean_data()

    def test_clean_data_no_numeric_columns(self):
        """Test con DataFrame sin columnas numéricas"""
        non_numeric_df = pd.DataFrame({
            'col1': ['a', 'b', 'c'],
            'col2': ['d', 'e', 'f']
        })
        cleaner = DiagnosticDataCleaner(non_numeric_df)
        with pytest.raises(ValueError, match="No hay columnas numéricas"):
            cleaner.clean_data()

    def test_clean_data_all_null_columns(self):
        """Test con DataFrame con todas las columnas nulas"""
        null_df = pd.DataFrame({
            'col1': [None, None, None],
            'col2': [None, None, None]
        })
        cleaner = DiagnosticDataCleaner(null_df)
        with pytest.raises(ValueError):
            cleaner.clean_data()