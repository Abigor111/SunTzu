"""Top-level package for SunTzu."""
# __init__.py
from .library_settings import read_file, Settings, start_Cleaning, start_netCDFMetadata, start_Optimization, start_ParquetMetadata, start_Statistics, start_Visualization, change_Settings
from .cleaning import Cleaning
from .metadata import netCDFMetadata, ParquetMetadata
from .statistics import Statistics
__author__ = "Igor Coimbra Carvalheira"
__email__ = "igorccarvalheira111@gmail.com"
__version__ = "0.5.0"
__all__ = ['Settings', 'Cleaning', 'netCDFMetadata', 'ParquetMetadata', 'read_file', 'Statistics', 'start_Cleaning', 'start_netCDFMetadata', 'start_Optimization', 'change_Settings','start_ParquetMetadata','start_Statistics','start_Visualization']

