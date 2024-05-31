import os
import pandas as pd
import xarray as xr
import pyarrow.parquet as pq
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDF_Metadata
from .metadata import ParquetMetadata
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
        
def read_file(path: str, **kwargs) -> xr.Dataset | pd.DataFrame:
    """
    Reads a file from the given path and returns the data in a structured format.

    Args:
        path (str): The path to the file to be read.
        kwargs: Additional options to customize the file reading process.

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
            return df
        elif extension == ".parquet":
            df = pd.read_parquet(path, **kwargs)
            return df
        elif extension == ".json":
            df = pd.read_json(path, **kwargs)
            return df
        elif extension == ".xlsx":
            df = pd.read_excel(path, **kwargs)
            return df
        elif extension == ".xml":
            df = pd.read_xml(path, **kwargs)
            return df
        elif extension == ".feather":
            df = pd.read_feather(path, **kwargs)
            return df
        elif extension == ".html":
            df = pd.read_html(path, **kwargs)
            return df
        elif extension == ".nc":
            df = xr.open_dataset(path, **kwargs)
            return df
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.")
    except Exception as e:
        raise RuntimeError(f"Error in reading the file {path}: {e}")