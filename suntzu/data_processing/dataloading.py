import polars as pl
class Loading(pl.DataFrame):
    @classmethod
    def read_file(cls, path, **kwargs):
        try:
            if path.endswith(".csv"):
                df = pl.read_csv(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".parquet"):
                df = pl.read_parquet(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".json"):
                df = pl.read_json(path, **kwargs).to_pandas()
            elif path.endswith(".xlsx"):
                df = pl.read_excel(path, **kwargs).to_pandas()
            elif path.endswith(".avro"):
                df = pl.read_avro(path, **kwargs).to_pandas()
            elif path.endswith(".arrow"):
                df = pl.read_ipc(path, **kwargs).to_pandas()
            else:
                raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, Json, Excel, Avro, Arrow")
        except Exception as e:
            raise RuntimeError(f"Error in reading the file {path}: {e}")

    def view(self):
        try:
            if self.is_empty():
                raise ValueError("No DataFrame loaded yet.")
            return self.head()
        except Exception as e:
            print(f"Error: {e}")

    def get_dims(self):
        try:
            if self.is_empty():
                raise ValueError("No DataFrame loaded yet.")
            print(f"Cols: {self.shape[1]}")
            print(f"Rows: {self.shape[0]}")
        except Exception as e:
            print(f"Error: {e}")



