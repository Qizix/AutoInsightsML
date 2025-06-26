import pandas as pd

class DataCleaner:
    def __init__(self, df: pd.DataFrame, column_types):
        self.df = df.copy()
        self.column_types = column_types
        
    def handle_missing(self, missing_strategy='mean') -> pd.DataFrame:
        for col in self.column_types['numerical']:
            if missing_strategy == 'mean':
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif missing_strategy == 'median':
                self.df[col] = self.df[col].fillna(self.df[col].median())
        for col in self.column_types['categorical']:
            self.df[col] = self.df[col].fillna('Unknown')
        return self.df


if __name__ == '__main__':
    from reader import DataLoader 
    dl = DataLoader('iris.csv')
    dc = DataCleaner(dl.df, dl.define_columns())
    print(dc.handle_missing().head())

        