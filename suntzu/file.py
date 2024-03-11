import os
import pandas as pd
import xarray as xr
import pyarrow.parquet as pq
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDF_Metadata
from .metadata import ParquetMetadata
class File:
    """
    A class that represents a file and provides methods and attributes for working with different file formats such as CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.

    Attributes:
        _df (pandas.DataFrame): The pandas DataFrame object representing the file data.
        _xr (xarray.Dataset): The xarray Dataset object representing the file data.
        statistics (Statistics): An instance of the Statistics class for performing statistical operations on the file data.
        cleaning (Cleaning): An instance of the Cleaning class for performing cleaning operations on the file data.
        metadata (ParquetMetadata or netCDF_Metadata): An instance of the ParquetMetadata class for accessing metadata of Parquet files or the netCDF_Metadata class for accessing metadata of NetCDF files.
    """
    def __init__(self, df):
        """
        Initializes a File object with a pandas DataFrame or an xarray Dataset.

        Args:
            df (pandas.DataFrame or xarray.Dataset): The data to be stored in the File object.
        """
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
        """
        Overrides the default attribute access behavior to provide access to statistics, cleaning, and metadata methods.

        Args:
            name (str): The name of the attribute to access.

        Returns:
            The attribute value if found.

        Raises:
            AttributeError: If the attribute is not found.
        """
        """
        This method provides access to dynamic attributes such as statistics, cleaning, and metadata methods.
        """
        if self._getattr_locked:
            return None
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
            self._getattr_locked = False
        
        raise AttributeError(f"{self} object has no attribute '{name}'")
    @staticmethod
    def get_file_extension(path):
        """
        Returns the file extension of a given file path.

        Args:
            path (str): The file path.

        Returns:
            str: The file extension.
        """
        return os.path.splitext(path)[1]

    def export_to_file(self, filename):
        """
        Exports data to a file with a specified filename.

        Args:
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
    Reads a file from the given path and returns the data in a structured format.

    Args:
        path (str): The path to the file to be read.
        **kwargs: Additional options to customize the file reading process.

    Returns:
        File object or list of tables: The data from the file in a structured format, except for HTML files where a list of tables is returned.

    Raises:
        ValueError: If the given path is not a valid file or the file format is not supported.
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
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.")
    except Exception as e:
        raise RuntimeError(f"Error in reading the file {path}: {e}")