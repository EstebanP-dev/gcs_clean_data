import pandas as pd

class DataCleaner:
    def __init__(self, data):
        self.data = data

    def clean(self) -> pd.DataFrame:
        self.data = self.data.dropna()
        return self.data
