import polars as pl
class TestDataFrame(pl.DataFrame):
    @classmethod
    def read_file(cls, path):
        try:
            df = pl.read_csv(path).to_pandas()
            return cls(df)
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
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


