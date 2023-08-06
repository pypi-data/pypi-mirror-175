# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = "psipy"
copyright = "2020, Predictive Science Inc."
author = "David Stansby"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_automodapi.automodapi",
    "sphinx_gallery.gen_gallery",
    "sphinx_rtd_theme",
    "numpydoc",
    "sphinx.ext.intersphinx",
]

numpydoc_show_class_members = False
sphinx_gallery_conf = {
    "examples_dirs": "../examples",
    "gallery_dirs": "auto_examples",
    "matplotlib_animations": True,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Raise an error for missing doc references
nitpicky = True
nitpick_ignore = [
    ("py:class", "Unit('deg')"),
    ("py:class", "Unit('m')"),
    ("py:class", "Unit('rad')"),
    # These are documented on websites in different namespaces
    # than where the classes are defined
    ("py:class", "astropy.units.core.Unit"),
    ("py:class", "pyvista.utilities.geometric_objects.Sphere"),
]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "xarray": ("https://xarray.pydata.org/en/stable/", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "heliopy": ("https://heliopy.readthedocs.io/en/0.15.4/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "streamtracer": ("https://streamtracer.readthedocs.io/en/stable/", None),
    "pyvista": ("https://docs.pyvista.org/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

default_role = "any"
automodapi_inheritance_diagram = False
automodsumm_inherited_members = True
