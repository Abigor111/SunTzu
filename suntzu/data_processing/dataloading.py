import polars as pl
class Dataloading(pl.DataFrame):
    @classmethod
    def read_file(cls, path):
        try:
            if path.endswith(".csv"):
                df = pl.read_csv(path).to_pandas()
                return cls(df)
            elif path.endswith(".parquet"):
                df = pl.read_parquet(path).to_pandas()
                return cls(df)
        except Exception as e:
            print(f"Error in reading the file: {e}")
            return cls(None)

    def view(self):
        if self.is_empty():
            print("Nenhum DataFrame carregado ainda.")
        else:
            return self.head()

    def get_dims(self):
        if self.is_empty():
            print("Nenhum DataFrame carregado ainda.")
        else:
            print(f"Cols: {self.shape[1]}")
            print(f"Rows: {self.shape[0]}")


