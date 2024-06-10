"""Top-level package for SunTzu."""
# __init__.py
from .library_settings import read_file, Settings
from .cleaning import Cleaning
from .metadata import netCDF_Metadata, ParquetMetadata
from .statistics import Statistics
__author__ = "Igor Coimbra Carvalheira"
__email__ = "igorccarvalheira111@gmail.com"
__version__ = "0.2.3"
__all__ = ['Settings', 'Cleaning', 'netCDF_Metadata', 'ParquetMetadata', 'read_file', 'Statistics']

