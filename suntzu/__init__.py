"""Top-level package for SunTzu."""
# __init__.py
#import pandas as pd
from .file import read_file, File
from .cleaning import Cleaning
from .metadata import netCDF_Metadata, ParquetMetadata
from .statistics import Statistics
__author__ = "Igor Coimbra Carvalheira"
__email__ = "igorccarvalheira111@gmail.com"
__version__ = "0.1.0"
__all__ = ['File', 'Cleaning', 'netCDF_Metadata', 'ParquetMetadata', 'capitalize_cols_name', 'read_file', 'PandasFile']

