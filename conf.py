# conf.py

import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'Spatial Data App'
author = 'Katarzyna Luszczewska'

# -- General configuration ---------------------------------------------------

# Add extensions here
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to the source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for extensions --------------------------------------------------

# Add custom settings for extensions, if needed.

# -- Options for autodoc extension -------------------------------------------

# Uncomment and modify if you have modules or packages to document
# autodoc_mock_imports = ['example_module']

# -- Options for napoleon extension ------------------------------------------

# Uncomment and modify if you want to use Google-style docstrings
napoleon_google_docstring = True

# -- Options for viewcode extension ------------------------------------------

# Uncomment and modify if you want to link to source code
# viewcode_follow_imported_members = False
