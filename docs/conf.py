import os, sys

project = 'SunTzu'
copyright = '2023-2024, Igor Carvalheira'
author = 'Igor Carvalheira'
release = '0.6.0'
sys.path.insert(0, os.path.abspath("../"))


extensions = ["sphinx.ext.napoleon", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = [] 

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']