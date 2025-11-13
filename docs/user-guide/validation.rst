.. _validation:

****************************
SOLARNET Metadata Validation
****************************

Overview
========

The SOLARNET :py:mod:`solarnet_metadata.validation` module provides tools to validate FITS files against the SOLARNET metadata schema requirements.
This ensures that your FITS files conform to the required standards and helps identify any issues with the metadata attributes.

The validation functions, without any additional options enabled, will validate FITS files and headers against the baseline SOLARNET schema requirements. 
For more stringent validation checks, you can enable additional warning options as needed. 
For validation against custom schema requirements, for example, if you have added custom mission-specific keywords, you can provide a custom schema to the validation functions. 
For more information on customizing the schema, see :ref:`solarnet_schema_customization`.

The validation process checks for:

- Required FITS and SOLARNET keywords must be included based on HDU type (primary, observation)
- Proper formatting of keywords, values, and comments
    - Keywords must be:
        - 1-8 characters in length
        - Contain only uppercase letters, digits, hyphens, and underscores  (A-Z, 0-9, -, _)
    - Values must be castable to string data types for inclusion in FITS headers
    - Comments must be castable to string data types for inclusion in FITS headers
    - The total FITS header line length (keyword + value + comment) must not exceed 80 characters
- Keyword values must match one of the expected valid values if specified in the schema
- Keyword values must match or be castable to the expected data type as defined in the schema

Using the Validation Functions
==============================

The main validation function is :py:func:`~solarnet_metadata.validation.validate_file`, which validates an entire FITS file.

This function returns a list of findings, which are strings describing any issues found during validation. 
If no issues are found, the list will be empty. 
Rather than raising exceptions for validation issues, the function collects all findings and returns them as a list. 
This allows you to see all issues at once rather than stopping at the first error. 
This can be extended in individual data processing pipelines to issue warnings or raise exceptions as needed.

The function assumes that the FITS file is structured according to standard FITS conventions, with a primary HDU and optional additional HDUs.

.. code-block:: python

    from pathlib import Path
    from solarnet_metadata.validation import validate_file

    # Path to the FITS file to validate
    fits_path = Path("/path/to/your/file.fits")

    # Validate the FITS file
    validation_findings: List[str] = validate_file(fits_path)

    # Print the validation findings
    print("Validation issues found:")
    for finding in validation_findings:
        print(finding)


Validation Options
------------------

The validation functions accept several parameters to control the validation process:
- :py:attr:`warn_empty_keyword` (bool): If :py:attr:`True`, the validator will issue warnings for any keywords that contain empty strings as values.
- :py:attr:`warn_no_comment` (bool): If :py:attr:`True`, the validator will issue warnings for any keywords that are missing comments.
- :py:attr:`warn_data_type` (bool): If :py:attr:`True`, the validator will check that keyword values match the expected data types defined in the schema.
- :py:attr:`warn_missing_optional` (bool): If :py:attr:`True`, the validator will issue warnings for optional keywords that aren't included, encouraging more complete metadata.
- :py:attr:`schema` (:py:class:`~solarnet_metadata.schema.SOLARNETSchema`): You can provide a custom schema instance to validate against custom requirements. If not provided, the default SOLARNET schema will be used.

.. code-block:: python

    from pathlib import Path
    from solarnet_metadata.validation import validate_file
    from solarnet_metadata.schema import SOLARNETSchema

    # Path to the FITS file to validate
    fits_path = Path("/path/to/your/file.fits")

    # Custom schema (optional)
    custom_schema = SOLARNETSchema()

    ## Validate with all warning options enabled
    validation_findings: List[str] = validate_file(
        file_path=fits_path,
        warn_empty_keyword=True,    # Report warnings for empty keywords
        warn_no_comment=True,       # Report warnings for missing comments
        warn_data_type=True,        # Validate data types against schema
        warn_missing_optional=True, # Report warnings for missing optional keywords
        schema=custom_schema        # Use custom schema (optional)
    )


Validating Individual Headers
-----------------------------

If you need to validate just a single FITS header, you can use the :py:func:`~solarnet_metadata.validation.validate_header` function.

This function takes an :py:class:`astropy.io.fits.Header` object and validates it against the schema requirements.

Specific options available for this function include:
- :py:attr:`is_primary` (bool): Set to :py:attr:`True` if the header is from a primary HDU, or :py:attr:`False` if it is from an observation HDU. This determines which keywords are required based on HDU type.
- :py:attr:`is_obs` (bool): Set to :py:attr:`True` if the header is from an observation HDU, or :py:attr:`False` if it is from a primary HDU. This determines which keywords are required based on HDU type. It is possible to set both :py:attr:`is_primary` and :py:attr:`is_obs` to :py:attr:`True` if the header is from a primary observation HDU.
- :py:attr:`warn_empty_keyword` (bool): If :py:attr:`True`, the validator will issue warnings for any keywords that contain empty strings as values.
- :py:attr:`warn_no_comment` (bool): If :py:attr:`True`, the validator will issue warnings for any keywords that are missing comments.
- :py:attr:`warn_data_type` (bool): If :py:attr:`True`, the validator will check that keyword values match the expected data types defined in the schema.
- :py:attr:`warn_missing_optional` (bool): If :py:attr:`True`, the validator will issue warnings for optional keywords that aren't included.
- :py:attr:`schema` (:py:class:`~solarnet_metadata.schema.SOLARNETSchema`): You can provide a custom schema instance to validate against custom requirements. If not provided, the default SOLARNET schema will be used.

.. code-block:: python

    from astropy.io import fits
    from solarnet_metadata.validation import validate_header

    # Open the FITS file and get the header
    with fits.open("/path/to/your/file.fits") as hdul:
        # Validate the primary header
        primary_findings: List[str] = validate_header(
            header=hdul[0].header,
            is_primary=True,
            is_obs=False,
            warn_data_type=True,
            warn_missing_optional=True,
        )
        
    # Print primary header findings
        print("Primary header issues:")
        for finding in primary_findings:
            print(finding)


Validating Keyword Format
-------------------------

You can validate individual FITS keywords, values, and comments using the :py:func:`~solarnet_metadata.validation.validate_fits_keyword_value_comment` function:

.. code-block:: python

    from solarnet_metadata.validation import validate_fits_keyword_value_comment

    # Example keyword, value, and comment
    keyword = "TELESCOP"
    value = "Solar Dynamics Observatory"
    comment = "Telescope name"

    # Validate the keyword, value, and comment
    findings: List[str] = validate_fits_keyword_value_comment(
        keyword=keyword, 
        value=value, 
        comment=comment,
        warn_empty_keyword=True,
        warn_no_comment=True
    )
    
    print("Validation issues:")
    for finding in findings:
        print(finding)


Checking Data Types
-------------------

To validate the data type of a keyword value against the schema:

.. code-block:: python

    from solarnet_metadata.validation import validate_fits_keyword_data_type
    from solarnet_metadata.schema import SOLARNETSchema

    # Optionally, create a custom schema instance
    custom_schema = SOLARNETSchema()

    # Example keyword and value
    keyword = "EXPTIME"
    value = 10.5

    # Validate the data type
    findings: List[str] = validate_fits_keyword_data_type(
        keyword=keyword,
        value=value,
        schema=custom_schema
    )
    
    print("Data type issues:")
    for finding in findings:
        print(finding)
