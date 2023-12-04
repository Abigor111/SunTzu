import polars as pl
import xarray as xr

class Loading(pl.DataFrame):
    @classmethod
    def read_file(cls, path, **kwargs):
        """
        Read a file and return a DataFrame object.

        Args:
            cls: The class to be instantiated with the DataFrame object.
            path: The path to the file.
            **kwargs: Additional keyword arguments to be passed to the file reader.

        Returns:
            An instance of the specified class with the DataFrame object.

        Raises:
            TypeError: If the path is not a string.
            ValueError: If the file format is not supported.
            RuntimeError: If there is an error in reading the file.
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string.")

        try:
            if path.endswith(".csv"):
                df = pl.read_csv(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".parquet"):
                df = pl.read_parquet(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".json"):
                df = pl.read_json(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".xlsx"):
                df = pl.read_excel(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".avro"):
                df = pl.read_avro(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith(".arrow"):
                df = pl.read_ipc(path, **kwargs).to_pandas()
                return cls(df)
            elif path.endswith("nc"):
                df = xr.open_dataset(path, **kwargs)
            else:
                raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, Json, Excel, Avro, Arrow")
        except Exception as e:
            raise RuntimeError(f"Error in reading the file {path}: {e}")
    def read_metadata(cls, path, **kwargs):
        pass