# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys

from docutils import nodes
from sphinx import addnodes

# Add the docs directory to the path for local imports
sys.path.insert(0, os.path.abspath("."))

from keyword_processor import process_documentation_files

# -- Project information -----------------------------------------------------

project = "SOLARNET Metadata"
copyright = "2024, Stein Vidar Hagfors Haugan, Terje Fredvik"
author = "Stein Vidar Hagfors Haugan, Terje Fredvik"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.graphviz",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["source"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "solarnet-emails.txt"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# GraphViz configuration
graphviz_output_format = "svg"  # 'svg' for HTML, 'png' for PDF

# Set automodapi to generate files inside the generated directory
automodapi_toctreedirnm = "generated/api"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    # Toc options
    "fixed_sidebar": True,
    "sidebar_width": "350px",
    "body_max_width": "none",
    "page_width": "95%",
    "show_relbars": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_logo = "logo/logo.png"
html_favicon = "logo/favicon.ico"

html_css_files = [
    "custom.css",
    "wide_navbar.css",
    "class_new_highlight.css",
]

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "letterpaper",
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "12pt",
    # Additional stuff for the LaTeX preamble.
    "classoptions": ",oneside",  # this avoids blank pages by using one-sided printing
    "extraclassoptions": "openany",  # prevents blank pages between chapters/sections
    "preamble": """
\setcounter{secnumdepth}{-1}
""",
    # Custom Margins to fit long code blocks
    "sphinxsetup": "hmargin={0.5in,0.5in}, vmargin={1in,1in}, marginpar=1in",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://data.astropy.org/intersphinx/python3.inv"),
    ),
    "numpy": (
        "https://docs.scipy.org/doc/numpy/",
        (None, "http://data.astropy.org/intersphinx/numpy.inv"),
    ),
    "scipy": (
        "https://docs.scipy.org/doc/scipy/reference/",
        (None, "http://data.astropy.org/intersphinx/scipy.inv"),
    ),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
    "sunpy": ("https://docs.sunpy.org/en/stable/", None),
}

# -- Generate CSV Files for Docs ---------------------------------------------


files_to_annotate = [
    "parta.md",
    "partb.md",
    "partc.md",
    "appendix-1.md",
    "appendix-2.md",
    "appendix-3.md",
    "appendix-4.md",
    "appendix-5.md",
    "appendix-6.md",
    "appendix-7.md",
    "appendix-8.md",
    "appendix-9.md",
]
# Process all the documentation files to extract and index keywords
process_documentation_files(files_to_annotate)

# -- Custom role for code indexing -------------------------------------------


def code_index_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    index_node = addnodes.index(entries=[("single", text, text, "", None)])
    code_node = nodes.literal(text, text)

    # Return both the index and code node
    return [index_node, code_node], []


def setup(app):
    """
    This function is called when Sphinx initializes the extension.
    We register our custom parser for indexing.
    """

    app.add_role("codeindex", code_index_role)
