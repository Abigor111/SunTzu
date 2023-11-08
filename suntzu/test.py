from polars import read_csv
class Test:
    def read_file(self, path):
        if path.endswith(".csv"):
            df = read_csv(path)
            df = df.to_pandas()
            return df
    def show(self):
        self.head()
