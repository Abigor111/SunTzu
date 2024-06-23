import os
import pandas as pd
import xarray as xr
import pyarrow.parquet as pq
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDF_Metadata
from .metadata import ParquetMetadata
from .optimization import Optimization
class Settings:
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

    def export_to_file(self: pd.DataFrame | xr.Dataset, filename: str):
        """
        Exports data to a file with a specified filename.

        Args:
            filename (str): The name of the file to export the data to.

        Raises:
            ValueError: If the file extension is not valid.
            FileExistsError: If the file already exists.
        """
        # List of valid file extensions
        suffixs = [".nc", ".parquet"]
        # Check if the filename exists
        if not os.path.isfile(filename):
            # Check if the filename has a valid file extension
            if self.get_file_extension(filename) in suffixs:
                # If the file extension is .nc, convert it to netCDF
                if self.get_file_extension(filename) == ".nc":
                    self.to_netcdf(filename)
                # If the file extension is .parquet, convert it to parquet
                elif self.get_file_extension(filename) == ".parquet":
                    pq.write_table(self, filename, compression=None)        
            # Raise an error if the file extension is invalid
            else:
                raise ValueError(f"Invalid file extension. Please provide a valid filename. Valid file extesions {suffixs}.")
        # Raise an error if the file already exists
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
    # Check if the given path is a file
    if not os.path.isfile(path):
        # Raise a ValueError if the path is not a file
        raise ValueError("Invalid file path.")

    try:
        # Get the file extension
        extension = Settings.get_file_extension(path)
        # If the extension is .csv, read the file as a CSV
        if extension == ".csv":
            df = pd.read_csv(path, **kwargs)
        # If the extension is .parquet, read the file as a Parquet
        elif extension == ".parquet":
            df = pd.read_parquet(path, **kwargs)
        # If the extension is .json, read the file as a JSON
        elif extension == ".json":
            df = pd.read_json(path, **kwargs)
        # If the extension is .xlsx, read the file as an Excel file
        elif extension == ".xlsx":
            df = pd.read_excel(path, **kwargs)
        # If the extension is .xml, read the file as an XML
        elif extension == ".xml":
            df = pd.read_xml(path, **kwargs)
        # If the extension is .feather, read the file as a Feather file
        elif extension == ".feather":
            df = pd.read_feather(path, **kwargs)
        # If the extension is .html, read the file as HTML
        elif extension == ".html":
            df = pd.read_html(path, **kwargs)
        # If the extension is .nc, read the file as a NetCDF file
        elif extension == ".nc":
            df = xr.open_dataset(path, **kwargs)
        # Raise a ValueError if the extension is not supported
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.")
        return df
    except Exception as e:
        # Raise a RuntimeError if there is an error reading the file
        raise RuntimeError(f"Error in reading the file {path}: {e}")