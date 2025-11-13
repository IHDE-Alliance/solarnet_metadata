"""
Process SOLARNET keywords in documentation files.

This module handles:
1. Loading keyword definitions from schema files
2. Scanning markdown files for keyword references
3. Adding index markers to keywords in output files
4. Generating CSV summaries of keywords and their usage locations
"""

import csv
import os
import re

from solarnet_metadata import data_directory
from solarnet_metadata.util import load_yaml_data


def load_solarnet_keywords():
    """Load keyword definitions from schema file and initialize reference tracking."""
    keywords = load_yaml_data(data_directory / "SOLARNET_attr_schema.yaml")[
        "attribute_key"
    ]

    # Initialize the references field for each keyword
    for key in keywords:
        keywords[key]["references"] = set()  # Use a set to avoid duplicates

    return keywords


def format_section_reference(section_id):
    """Format a section ID into a readable reference link."""
    if section_id.startswith("appendix-"):
        appendix_name = section_id.replace("appendix-", "")

        if "-" in appendix_name:
            # Handle sub-appendices like 'vi-a'
            main_part, sub_part = appendix_name.split("-", 1)
            display_name = f"Appendix {main_part.upper()}-{sub_part}"
        else:
            # Check for letter suffix (like 'ia', 'vib')
            match = re.match(r"([ivx]+)([a-z]*)", appendix_name)
            if match:
                roman_part, letter_part = match.group(1), match.group(2)

                if letter_part:
                    display_name = f"Appendix {roman_part.upper()}-{letter_part}"
                else:
                    display_name = f"Appendix {roman_part.upper()}"
            else:
                display_name = f"Appendix {appendix_name.upper()}"

        return f"[{display_name}](#{section_id})"
    else:
        # For numeric sections, keep the same format
        return f"[{section_id}](#{section_id})"


def find_sections_in_file(content):
    """Extract section positions and references from file content."""
    section_positions = []
    current_section = None
    lines = content.split("\n")

    for i, line in enumerate(lines):
        section_match = re.search(
            r"\(((?:[0-9]+\.[0-9]+(?:\.[0-9]+)*)|(?:appendix-[a-z0-9-]+))\)=", line
        )
        if section_match:
            current_section = section_match.group(1)
            current_section_ref = format_section_reference(current_section)

        if current_section:
            section_positions.append((i, current_section_ref))

    return section_positions, lines


def process_keywords_in_file(file_path, solarnet_keywords):
    """Process a markdown file to identify keyword references and add index markers."""
    with open(file_path, "r", encoding="utf-8") as input_file:
        source_content = input_file.read()

    section_positions, lines = find_sections_in_file(source_content)

    # Find keyword mentions and associate them with sections
    for keyword in solarnet_keywords:
        keyword_text = keyword.strip("`")
        keyword_pattern_plain = re.compile(r"\b" + re.escape(keyword_text) + r"\b")
        keyword_pattern_backticks = re.compile(r"`" + re.escape(keyword_text) + r"`")

        in_code_block = False
        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Use appropriate pattern based on context
            pattern = (
                keyword_pattern_plain if in_code_block else keyword_pattern_backticks
            )
            matches = pattern.findall(line)

            if matches:
                # Find nearest section above this line
                nearest_section = None
                for pos, section_ref in section_positions:
                    if pos <= i:
                        nearest_section = section_ref
                    else:
                        break

                if nearest_section:
                    solarnet_keywords[keyword]["references"].add(nearest_section)

    # Create the output file with indexed keywords
    output_file_path = os.path.join("generated", os.path.basename(file_path))
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        # Split by code blocks and only process non-code parts
        code_block_pattern = re.compile(r"(```.*?```)", re.DOTALL)
        parts = code_block_pattern.split(source_content)

        for i in range(len(parts)):
            if not code_block_pattern.match(parts[i]):
                # Replace keywords with indexed versions outside code blocks
                for key in solarnet_keywords:
                    parts[i] = parts[i].replace(f"`{key}`", f"{{codeindex}}`{key}`")

        output_file.write("".join(parts))


def section_reference_sort_key(ref):
    """Sort key function for ordering section references."""
    match = re.search(r"\[(.*?)\]", ref)
    if not match:
        return (999, ref)  # Default case for unexpected formats

    section_text = match.group(1)

    if section_text.startswith("Appendix "):
        return (2, section_text)  # Appendices come after numeric sections

    # For numeric sections (like 3.1, 18.7)
    try:
        parts = [int(part) for part in section_text.split(".")]
        while len(parts) < 3:
            parts.append(0)
        return (1, parts[0], parts[1], parts[2])  # Numeric sections come first
    except ValueError:
        return (999, section_text)


def generate_keyword_csv(solarnet_keywords, output_path):
    """Generate a CSV file with keyword information and references."""
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write each keyword and its information
        for keyword, data in sorted(
            solarnet_keywords.items(), key=lambda x: x[0].strip("`").lower()
        ):
            keyword_references = data["references"]
            formatted_refs = (
                ", ".join(sorted(keyword_references, key=section_reference_sort_key))
                if keyword_references
                else ""
            )
            writer.writerow(
                [
                    f"`{keyword}`",
                    f"`{data['origin']}`",
                    data["description"],
                    f"`{data['required']}`",
                    formatted_refs,
                ]
            )


def process_documentation_files(files_to_process):
    """Process all documentation files to extract and index keywords."""
    # Create output directory if it doesn't exist
    if not os.path.exists("generated"):
        os.mkdir("generated")

    # Load keyword definitions
    solarnet_keywords = load_solarnet_keywords()

    # Process each documentation file
    for file in files_to_process:
        file_path = f"source/{file}"
        process_keywords_in_file(file_path, solarnet_keywords)

    # Generate the CSV summary
    generate_keyword_csv(solarnet_keywords, "generated/solarnet_keyword_list.csv")

    return solarnet_keywords
