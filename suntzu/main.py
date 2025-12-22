import pandas as pd

import os

from .cleaning import Cleaning
from .statistics import Statistics
from .settings import Settings

# Main Code
class Suntzu(pd.DataFrame):
    def clean(self):
        return Cleaning(self)
    def stats(self):
        return Statistics(self)
def read_file(path: str, **kwargs) -> Suntzu:
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
        extension = Settings.get_file_extension(path)
        valid_extensions = {
            ".csv": pd.read_csv,
            ".json": pd.read_json,
            ".xlsx": pd.read_excel,
            ".xml": pd.read_xml,
            ".feather": pd.read_feather,
            ".parquet": pd.read_parquet
        }
        if extension in valid_extensions:
            return Suntzu(valid_extensions[extension](path, **kwargs))
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML and Feather.")
    except Exception as e:
        raise RuntimeError(f"Error in reading the file {path}: {e}")