import polars as pl
class Loading(pl.DataFrame):
    @classmethod
    def read_file(cls, path):
        try:
            if path.endswith(".csv"):
                df = pl.read_csv(path).to_pandas()
                return cls(df)
            elif path.endswith(".parquet"):
                df = pl.read_parquet(path).to_pandas()
                return cls(df)
            else:
                raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet")
        except Exception as e:
            raise RuntimeError(f"Error in reading the file {path}: {e}")

    def view(self):
        if self.is_empty():
                print("No DataFrame loaded yet.")
        else:
            return self.head()

    def get_dims(self):
        if self.is_empty():
            print("No DataFrame loaded yet.")
        else:
            print(f"Cols: {self.shape[1]}")
            print(f"Rows: {self.shape[0]}")


