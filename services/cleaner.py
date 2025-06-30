import pandas as pd

class DataCleaner:
    def __init__(self, df: pd.DataFrame, column_types):
        self.df = df
        self.column_types = column_types

    def handle_missing(self, missing_strategy_num='mean', missing_strategy_cat='Unknown') -> pd.DataFrame:
        for col in self.column_types['numerical']:
            if missing_strategy_num == 'mean':
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif missing_strategy_num == 'median':
                self.df[col] = self.df[col].fillna(self.df[col].median())

        for col in self.column_types['categorical']:
            if missing_strategy_cat == "Unknown":
                self.df[col] = self.df[col].fillna('Unknown')
            elif missing_strategy_cat == "mode":
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

        return self.df


if __name__ == '__main__':
    from reader import DataLoader
    dl = DataLoader('iris.csv')
    dc = DataCleaner(dl.df, dl.define_columns())
    print(dc.handle_missing().head())

