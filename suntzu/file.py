import os
import pandas as pd
import xarray as xr
import pyarrow.parquet as pq
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDF_Metadata
from .metadata import ParquetMetadata
class File:
    def __init__(self, df):
        if isinstance(df, pd.DataFrame):
            self._df = df
            self.statistics = Statistics(df)
            self.cleaning = Cleaning(df)
            self.metadata = ParquetMetadata(df)
        elif isinstance(df, xr.Dataset):
            self._xr = df
            self.metadata = netCDF_Metadata(df)
        self._getattr_locked = False
    def __getattr__(self, name):
        # Verificar se o método __getattr__ está bloqueado
        if self._getattr_locked:
            return None
        # Bloquear o método __getattr__ para evitar recursão infinita
        self._getattr_locked = True
        try:
            if hasattr(self, '_df') and name != '_df':
                if hasattr(self.statistics, name):
                    return getattr(self.statistics, name)
                elif hasattr(self.cleaning, name):
                    return getattr(self.cleaning, name)
                elif hasattr(self.metadata, name):
                    return getattr(self.metadata, name)
            elif hasattr(self, '_xr'):
                if hasattr(self.metadata, name):
                    return getattr(self.metadata, name)
        finally:
            # Desbloquear o método __getattr__ após a execução
            self._getattr_locked = False
        
        # Se nenhum atributo for encontrado, levantamos um AttributeError
        raise AttributeError(f"'File' object has no attribute '{name}'")

    def get_file_extension(path):
        return os.path.splitext(path)[1]
    def export_to_file(self, filename):
        """
        Exports data to a file with a specified filename.

        Args:
            self: The data object that needs to be exported.
            filename (str): The name of the file to export the data to.

        Raises:
            ValueError: If the file extension is not valid.
            FileExistsError: If the file already exists.
        """
        suffixs = [".nc", ".parquet"]
        if not os.path.isfile(filename):
            if self.get_file_extension(filename) in suffixs:
                if self.get_file_extension(filename) == ".nc":
                    self.to_netcdf(filename)
                elif self.get_file_extension(filename) == ".parquet":
                    pq.write_table(self, filename, compression=None)        
            else:
                raise ValueError(f"Invalid file extension. Please provide a valid filename. Valid file extesions {suffixs}.")
        else:
            raise FileExistsError(f"{filename} already exists. Please change it or delete it.")
def read_file(path, **kwargs):
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
    if not os.path.isfile(path):
        raise ValueError("Invalid file path.")

    try:
        extension = File.get_file_extension(path)
        if extension == ".csv":
            df = pd.read_csv(path, **kwargs)
            return File(df)
        elif extension == ".parquet":
            df = pd.read_parquet(path, **kwargs)
            return File(df)
        elif extension == ".json":
            df = pd.read_json(path, **kwargs)
            return File(df)
        elif extension == ".xlsx":
            df = pd.read_excel(path, **kwargs)
            return File(df)
        elif extension == ".xml":
            df = pd.read_xml(path, **kwargs)
            return File(df)
        elif extension == ".feather":
            df = pd.read_feather(path, **kwargs)
            return File(df)
        elif extension == ".html":
            df = pd.read_html(path, **kwargs)
            return pd.read_html(path, **kwargs)
        elif extension == ".nc":
            df = xr.open_dataset(path, **kwargs)
            return File(df)
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, Json, Excel, Avro, Arrow")
    except Exception as e:
        raise RuntimeError(f"Error in reading the file {path}: {e}")