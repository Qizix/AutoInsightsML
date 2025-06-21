import pandas as pd

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.column_types = {}
        
    def load(self):
        self.df = pd.read_csv(self.file_path)
    
    def define_columns(self):
        self.column_types['numerical'] = self.df.select_dtypes(include='number').columns.tolist()
        self.column_types['categorical'] = self.df.select_dtypes(include='object').columns.tolist()
        return self.column_types
    
    def check_nulls(self):
        return self.df.isnull().sum()