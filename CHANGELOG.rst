This project uses `semantic versioning <https://semver.org>`_. 

Latest
======

* Added Python package structure with validation and schema functionality:
    * New ``solarnet_metadata.schema`` module with ``SOLARNETSchema`` class for attribute schema handling
    * New ``solarnet_metadata.validation`` module for FITS header validation against SOLARNET requirements
    * Comprehensive YAML schema definition for all SOLARNET metadata attributes
* Added CI/CD GitHub Actions workflows:
    * Codestyle and linting (``black``, ``flake8``)
    * Documentation building
    * Cross-platform testing with multiple Python versions
* Improved documentation:
    * Reorganized structure with API, User, and Developer guides
    * Enhanced navigation and styling
* Added build configuration with ``pyproject.toml`` for modern Python packaging
* Added pre-commit configuration for code quality
* Converted Section 19 Keyword List generation. 
    * Added "Required" column to keyword listing in Section 19
    * Previously, this keyword list was generated using a CSV file and some python code to generate the "Section Reference" list. 
    * This CSV file has been replaced with the larger "schema" YAML file, which contains a larger set of metadata about each keyword. The Python code for generating the keyword list in Section 19 has been updated to read from this schema file.
    * Future updates to add or remove keywords should be done in the schema file. `solarnet_metadata/data/SOLARNET_attr_schema.yaml`

3.1.0 (2025-06-25)
==================

* Add wide and sticky nav bar (#24)
* Add Zenodo References for citation attribution (#20)
* Parent extensions (PARENTXT), external extensions, Type P data exemption - use PARENTXT (#23)
* Explain that PARENTXT can refer to non-FITS files (no extension name) (#27)
* Auto-Generate Section References for Part C. / Section 19. (#28)
* Add Development & Version Guidelines (#36)

3.0.0 (2025-02-04)
==================

* Conversion of the SOLARNET metadata standard from its original word file format into a repository to enable issue tracking and version control. This release preserves the original content as written by Stein Haugan and Terje Fredvik.
* Updated License to CC BY 4.0 (#16)
* Added issue templates (#7, #10)
* Added text of the original word file for the Solarnet recommendations (#5)
