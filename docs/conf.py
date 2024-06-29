# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
project = 'SunTzu'
copyright = '2023-2024, Igor Carvalheira'
author = 'Igor Carvalheira'
release = '0.5.0'
sys.path.insert(0, os.path.abspath("../"))
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.napoleon", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = [] # '_build','Thumbs.db', '.DS_Store'



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
