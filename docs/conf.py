# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute.

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "stinger-ipc"
copyright = f"{datetime.now().year}, Jacob Davis"
author = "Jacob Davis"

# The full version, including alpha/beta/rc tags, read dynamically from the
# installed package so it stays in sync with pyproject.toml.  Falls back to
# "unknown" when the package isn't installed (e.g. fresh CI checkout).
try:
    release = version("stinger-ipc")
except PackageNotFoundError:
    release = "unknown"
# The short X.Y version.
version = release

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Suppress benign warnings that don't affect the rendered output:
#  - architecture.md uses ```plantuml``` fenced blocks, which Pygments
#    cannot lex; the blocks are rendered without syntax highlighting.
#  - sphinx_autodoc_typehints warns about pydantic-internal forward
#    references and guarded imports (JsonValue, _PartialClsOrStaticMethod,
#    etc.) that are not part of this project's code.
suppress_warnings = [
    "misc.highlighting_failure",
    "sphinx_autodoc_typehints.forward_reference",
    "sphinx_autodoc_typehints.guarded_import",
]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for autodoc -----------------------------------------------------

# Always document members inherited from base classes only if they are
# explicitly listed. Keep generated API docs focused.
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": True,
}

# Do not prepend module names to object names in the API reference.
add_module_names = False

# -- Options for autosummary -------------------------------------------------

autosummary_generate = True

# -- Options for napoleon ----------------------------------------------------

# Parse Google- and NumPy-style docstrings in addition to reStructuredText.
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}
