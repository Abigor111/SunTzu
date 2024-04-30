import os
import pandas as pd
import xarray as xr
import pyarrow.parquet as pq
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDF_Metadata
from .metadata import ParquetMetadata

# class DataFrameFile:
#     def __init__(self, df: pd.DataFrame):
#         """
#         Initializes a File object with a pandas DataFrame.

#         Args:
#             df (pandas.DataFrame or xarray.Dataset): The data to be stored in the File object.
#         """
#         super().__init__()

#         self.df = df
#         self.statistics = Statistics(df)
#         self.cleaning = Cleaning(df)
#         self.parquet_metadata = ParquetMetadata(df)

#     def __getattr__(self, name):
#         return getattr(self.df, name)

class PandasFile:
    """
    A class that represents a file and provides methods and attributes for working with different file formats such as CSV, Parquet, JSON, Excel, XML, Feather, excluding netCDF_Metadata.

    Attributes:
        _df (pandas.DataFrame): The pandas DataFrame object representing the file data.
        _xr (xarray.Dataset): The xarray Dataset object representing the file data.
        statistics (Statistics): An instance of the Statistics class for performing statistical operations on the file data.
        cleaning (Cleaning): An instance of the Cleaning class for performing cleaning operations on the file data.
        metadata (ParquetMetadata): An instance of the ParquetMetadata class for accessing metadata of Parquet files.
    """

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.statistics = Statistics(df)
        self.cleaning = Cleaning(df)
        # if isinstance(df, pd.DataFrame):
        self.metadata = ParquetMetadata(df)
        # elif isinstance(df, xr.Dataset):
            # raise ValueError("PandasFile does not support xarray Dataset.")
    def capitalize_cols_name(self, cols = None):
        """
        Capitalizes the column names of the DataFrame.

        Parameters:
            cols (list, optional): List of column names to be capitalized. If None, all columns will be capitalized. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame with capitalized column names.
        """
        return self.cleaning.capitalize_cols_name()
class Xarray:
    """
    A class that represents a file and provides methods and attributes for working with different file formats such as CSV, Parquet, JSON, Excel, XML, Feather, excluding ParquetMetadata.

    Attributes:
        _df (pandas.DataFrame): The pandas DataFrame object representing the file data.
        _xr (xarray.Dataset): The xarray Dataset object representing the file data.
        statistics (Statistics): An instance of the Statistics class for performing statistical operations on the file data.
        cleaning (Cleaning): An instance of the Cleaning class for performing cleaning operations on the file data.
        metadata (netCDF_Metadata): An instance of the netCDF_Metadata class for accessing metadata of NetCDF files.
    """

    def __init__(self, ds):
        self._ds = ds
        self.statistics = Statistics(ds)
        self.cleaning = Cleaning(ds)
        if isinstance(ds, xr.Dataset):
            self.metadata = netCDF_Metadata(ds)
        elif isinstance(ds, pd.DataFrame):
            raise ValueError("FileWithoutParquet does not support pandas Dataframe.")
        

class File:
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
        
from typing import Union
def read_file(path: str, **kwargs) -> 'Union[Xarray, PandasFile]':
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
            return PandasFile(df)
        elif extension == ".parquet":
            df = pd.read_parquet(path, **kwargs)
            return df
        elif extension == ".json":
            df = pd.read_json(path, **kwargs)
            return PandasFile(df)
        elif extension == ".xlsx":
            df = pd.read_excel(path, **kwargs)
            return PandasFile(df)
        elif extension == ".xml":
            df = pd.read_xml(path, **kwargs)
            return PandasFile(df)
        elif extension == ".feather":
            df = pd.read_feather(path, **kwargs)
            return PandasFile(df)
        elif extension == ".html":
            df = pd.read_html(path, **kwargs)
            return PandasFile(df)
        elif extension == ".nc":
            df = xr.open_dataset(path, **kwargs)
            return Xarray(df)
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.")
    except Exception as e:
        raise RuntimeError(f"Error in reading the file {path}: {e}")