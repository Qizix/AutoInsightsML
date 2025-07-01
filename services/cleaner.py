import pandas as pd

class DataCleaner:
    def __init__(self, df: pd.DataFrame, column_types):
        self.df = df
        self.column_types = column_types

    def handle_missing(
        self, missing_strategy_num="mean", missing_strategy_cat="Unknown"
    ) -> pd.DataFrame:
        for col in self.column_types["numerical"]:
            if missing_strategy_num == "mean":
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif missing_strategy_num == "median":
                self.df[col] = self.df[col].fillna(self.df[col].median())

        for col in self.column_types["categorical"]:
            if missing_strategy_cat == "mode":
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
            else:
                self.df[col] = self.df[col].fillna(missing_strategy_cat)

        return self.df

    def drop_with_missing_data(self, drop_rate: float, axis: int) -> pd.DataFrame:
        # drop_rate - how much % NA needed to delete
        thresh = int((1 - drop_rate) * self.df.shape[axis - 1])
        print(thresh)
        return self.df.dropna(axis=axis, thresh=thresh)


if __name__ == "__main__":
    from reader import DataLoader

    dl = DataLoader("iris.csv")
    dc = DataCleaner(dl.df, dl.define_columns())
    print(dl.df.shape)
    print(dc.drop_rows_with_missing_data(0.3, 0))
