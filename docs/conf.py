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
import os

# import sys
# sys.path.insert(0, os.path.abspath('.'))

from docutils import nodes
from sphinx.util.texescape import escape
from sphinx import addnodes

# -- Project information -----------------------------------------------------

project = "Solarnet"
copyright = "2024, Stein Vidar Hagfors Haugan, Terje Fredvik"
author = "Stein Vidar Hagfors Haugan, Terje Fredvik"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["source"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    # Toc options
    'fixed_sidebar': True,
    'sidebar_width': '350px',
    'body_max_width' : 'none',
    'page_width': '95%',
} 

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

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

# -- Generate CSV Files for Docs ---------------------------------------------
import csv
import re

if not os.path.exists("generated"):
    os.mkdir("generated")  # generate the directory before putting things in it

solarnet_keywords = []
with open("solarnet_keyword_list.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
    for row in spamreader:
        kywd = row[0].rstrip()
        solarnet_keywords.append(kywd)

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
for file in files_to_annotate:
    with open(f"source/{file}", "r") as input_file:
        with open(f"generated/{file}", "w") as output_file:
            whole_file_str = input_file.read()

            # Function to replace keywords outside of code blocks
            def replace_keywords(text):
                for this_key in solarnet_keywords:
                    text = re.sub(rf"{this_key}", f"{{codeindex}}`{this_key}`", text)
                return text

            # Define a regex pattern to match code blocks
            code_block_pattern = re.compile(r"(```.*?```)", re.DOTALL)
            # Split the file into segments using the code block pattern
            parts = code_block_pattern.split(whole_file_str)
            # Apply replacements only to non-code block parts
            for i in range(len(parts)):
                if not code_block_pattern.match(
                    parts[i]
                ):  # If the part is not a code block
                    parts[i] = replace_keywords(parts[i])

            # Rejoin the parts and write to the output file
            output_file.write("".join(parts))


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
    app.add_css_file('wide_navbar.css')
    app.add_css_file('class_new_highlight.css')
