"""Top-level package for SunTzu."""
# __init__.py
from .library_settings import read_file, Settings, start_Cleaning, start_netCDFMetadata, start_Optimization, start_ParquetMetadata, start_Statistics, start_Visualization, change_Settings
from .cleaning import Cleaning
from .metadata import netCDFMetadata, ParquetMetadata
from .statistics import Statistics

__author__ = "Igor Coimbra Carvalheira"
__email__ = "igorccarvalheira111@gmail.com"
__version__ = "0.8.0pypi-AgEIcHlwaS5vcmcCJDkwZjRjN2VhLTM1MGQtNDljNy04NTMyLTNmZDgyMTk3MTQzMgACDlsxLFsic3VudHp1Il1dAAIsWzIsWyI4M2U2YzkzZS04MGM1LTRjODQtYWYwZi02ZGE3ZTUyNzNlOGEiXV0AAAYgz72ld2M6SU6i4OJjyJr3jOzWsxrn3pn0c4ZiwroIaUc"
__all__ = ['Settings', 'Cleaning', 'netCDFMetadata', 'ParquetMetadata', 'read_file', 'Statistics', 'start_Cleaning', 'start_netCDFMetadata', 'start_Optimization', 'change_Settings','start_ParquetMetadata','start_Statistics','start_Visualization']

