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
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

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
import csv
import re

if not os.path.exists("generated"):
    os.mkdir("generated")  # generate the directory before putting things in it

solarnet_keywords = {}
with open("solarnet_keyword_list.csv", "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        if len(row) != 3:
            raise ValueError(f"Expected 3 columns in CSV file, got {len(row)}: {row}")
        # Split Row
        kywd = row[0].rstrip()
        origin, description = row[1].rstrip(), row[2].rstrip()
        solarnet_keywords[kywd] = {
            "origin": origin,
            "description": description,
            "references": set(),  # Stub references as empty set
        }

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
    with open(f"source/{file}", "r", encoding="utf-8") as input_file:
        source_content = input_file.read()

        # Create a mapping from position to section reference
        section_positions = []
        current_section = None
        lines = source_content.split("\n")

        for i, line in enumerate(lines):
            section_match = re.search(
                r"\(((?:[0-9]+\.[0-9]+(?:\.[0-9]+)*)|(?:appendix-[a-z0-9-]+))\)=", line
            )
            if section_match:
                current_section = section_match.group(1)

                # Format the reference differently based on section type
                if current_section.startswith("appendix-"):
                    # For appendix sections, format as [Appendix X](#appendix-x)
                    appendix_name = current_section.replace("appendix-", "")

                    # Handle Roman numerals properly
                    if "-" in appendix_name:
                        # Handle sub-appendices like 'vi-a' properly
                        main_part, sub_part = appendix_name.split("-", 1)
                        # Convert the main Roman numeral to uppercase
                        display_name = f"Appendix {main_part.upper()}-{sub_part}"
                    else:
                        # First check if there's a letter suffix (like 'ia', 'vib')
                        match = re.match(r"([ivx]+)([a-z]*)", appendix_name)
                        if match:
                            roman_part = match.group(1)
                            letter_part = match.group(2)

                            if letter_part:
                                # It's a sub-appendix with format like 'ia', 'vib'
                                display_name = (
                                    f"Appendix {roman_part.upper()}-{letter_part}"
                                )
                            else:
                                # It's a main appendix
                                display_name = f"Appendix {roman_part.upper()}"
                        else:
                            # Fallback for any other format
                            display_name = f"Appendix {appendix_name.upper()}"

                    current_section_ref = f"[{display_name}](#{current_section})"
                else:
                    # For numeric sections, keep the same format
                    current_section_ref = f"[{current_section}](#{current_section})"

            if current_section:
                section_positions.append((i, current_section_ref))

        # Find keyword mentions and associate them with the nearest section above
        for keyword in solarnet_keywords:
            # Create patterns for both with and without backticks
            keyword_text = keyword.strip("`")  # Remove backticks if present
            keyword_pattern_plain = re.compile(r"\b" + re.escape(keyword_text) + r"\b")
            keyword_pattern_backticks = re.compile(
                r"`" + re.escape(keyword_text) + r"`"
            )

            # Track if we're inside a code block
            in_code_block = False

            for i, line in enumerate(lines):
                # Check if this line starts or ends a code block
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue

                # Use the appropriate pattern based on whether we're in a code block
                if in_code_block:
                    matches = keyword_pattern_plain.findall(line)
                else:
                    matches = keyword_pattern_backticks.findall(line)

                if matches:
                    # Find the nearest section above this line
                    nearest_section = None
                    for pos, section_ref in section_positions:
                        if pos <= i:
                            nearest_section = section_ref
                        else:
                            break

                    if nearest_section:
                        solarnet_keywords[keyword]["references"].add(nearest_section)

        with open(f"generated/{file}", "w", encoding="utf-8") as output_file:

            # Function to replace keywords outside of code blocks
            def replace_keywords(text):
                for this_key in solarnet_keywords:
                    text = re.sub(rf"{this_key}", f"{{codeindex}}`{this_key}`", text)
                return text

            # Define a regex pattern to match code blocks
            code_block_pattern = re.compile(r"(```.*?```)", re.DOTALL)
            # Split the file into segments using the code block pattern
            parts = code_block_pattern.split(source_content)
            # Apply replacements only to non-code block parts
            for i in range(len(parts)):
                if not code_block_pattern.match(
                    parts[i]
                ):  # If the part is not a code block
                    parts[i] = replace_keywords(parts[i])

            # Rejoin the parts and write to the output file
            output_file.write("".join(parts))

# Make a copy for direct inclusion in the documentation
with open(
    "generated/solarnet_keyword_list.csv", "w", newline="", encoding="utf-8"
) as csvfile:
    writer = csv.writer(csvfile)

    # Define a custom sorting function for references
    def section_reference_sort_key(ref):
        # Extract the section identifier from the reference
        match = re.search(r"\[(.*?)\]", ref)
        if not match:
            return (999, ref)  # Default case for unexpected formats

        section_text = match.group(1)

        # Check if it's an appendix reference
        if section_text.startswith("Appendix "):
            return (2, section_text)  # Appendices come after numeric sections

        # For numeric sections (like 3.1, 18.7)
        try:
            # Convert each part to an integer for proper numeric ordering
            parts = [int(part) for part in section_text.split(".")]
            # Pad with zeros to handle different section depths
            while len(parts) < 3:
                parts.append(0)
            return (1, parts[0], parts[1], parts[2])  # Numeric sections come first
        except ValueError:
            # Fallback for anything else
            return (999, section_text)

    # Loop each keyword and write to the CSV
    for keyword, data in sorted(
        solarnet_keywords.items(), key=lambda x: x[0].strip("`").lower()
    ):
        keyword_references = data["references"]
        # Sort references using the custom sorting function
        formatted_refs = (
            ", ".join(sorted(keyword_references, key=section_reference_sort_key))
            if keyword_references
            else ""
        )
        writer.writerow([keyword, data["origin"], data["description"], formatted_refs])


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
