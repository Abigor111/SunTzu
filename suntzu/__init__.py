"""Top-level package for SunTzu."""
# __init__.py
from .settings import Settings
from .cleaning import Cleaning
from .metadata import ParquetMetadata
from .statistics import Statistics
from .main import Suntzu, read_file

__author__ = "Igor Coimbra Carvalheira"
__email__ = "igorccarvalheira111@gmail.com"
__version__ = "1.0.0"
__all__ = ['Settings', 'Cleaning', 'ParquetMetadata', 'read_file', 'Statistics', 'Suntzu']