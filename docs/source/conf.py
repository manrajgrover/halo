# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import recommonmark
from recommonmark.transform import AutoStructify

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'halo'
copyright = '2019, Manraj Singh'
author = 'Manraj Singh'

# TODO: Single source version info
# The short X.Y version
version = '0.0'

# The full version, including alpha/beta/rc tags
release = '0.0.28'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'recommonmark',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Handle mapping of external module documentation written with Sphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# Document private members
autodoc_default_flags = [
    'members',
    'private-members'
]

# Define master document
master_doc = 'index'

# Document class' and __init__ docstrings combined
autoclass_content = 'both'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

def setup(app):
    app.add_config_value('recommonmark_config', {
            'auto_toc_tree_section': 'Contents',
            'enable_eval_rst': True,
            }, True)
    app.add_transform(AutoStructify)
