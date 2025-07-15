.. validation:

*****************************************************
Using SOLARNET Validator for FITS Metadata Validation
*****************************************************

Overview
========

The SOLARNET :py:mod:`solarnet_metadata.validation` module provides tools to validate FITS files against the SOLARNET metadata schema requirements.
This ensures that your FITS files conform to the required standards and helps identify any issues with the metadata attributes.

The validation process checks for:

- Required keywords based on HDU type (primary, observation)
- Pattern-based keywords when specified in the schema
- Proper formatting of keywords, values, and comments
- Correct data types for keyword values

Using the Validation Functions
==============================

The main validation function is :py:func:`~solarnet_metadata.validation.validate_file`, which validates an entire FITS file.

.. code-block:: python

    from pathlib import Path
    from solarnet_metadata.validation import validate_file

    # Path to the FITS file to validate
    fits_path = Path("/path/to/your/file.fits")

    # Validate the FITS file
    validation_findings: List[str] = validate_file(fits_path)

    # Print the validation findings
    if validation_findings:
        print("Validation issues found:")
        for finding in validation_findings:
            print(finding)
    else:
        print("No validation issues found.")

Validation Options
------------------

The validation functions accept several parameters to control the validation process:

.. code-block:: python

    from pathlib import Path
    from solarnet_metadata.validation import validate_file
    from solarnet_metadata.schema import SOLARNETSchema

    # Path to the FITS file to validate
    fits_path = Path("/path/to/your/file.fits")

    # Custom schema (optional)
    custom_schema = SOLARNETSchema()

    # Validate with all warning options enabled
    validation_findings = validate_file(
        file_path=fits_path,
        warn_empty_keyword=True,    # Report warnings for empty keywords
        warn_no_comment=True,       # Report warnings for missing comments
        warn_data_type=True,        # Validate data types against schema
        schema=custom_schema        # Use custom schema (optional)
    )

Validating Individual Headers
-----------------------------

If you need to validate just a single FITS header, you can use the :py:func:`~solarnet_metadata.validation.validate_header` function:

.. code-block:: python

    from astropy.io import fits
    from solarnet_metadata.validation import validate_header

    # Open the FITS file and get the header
    with fits.open("/path/to/your/file.fits") as hdul:
        # Validate the primary header
        primary_findings = validate_header(
            header=hdul[0].header,
            is_primary=True,
            warn_data_type=True
        )
        
        # Print primary header findings
        if primary_findings:
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
    findings = validate_fits_keyword_value_comment(
        keyword=keyword, 
        value=value, 
        comment=comment,
        warn_empty_keyword=True,
        warn_no_comment=True
    )
    
    if findings:
        print("Validation issues:")
        for finding in findings:
            print(finding)

Checking Data Types
-------------------

To validate the data type of a keyword value against the schema:

.. code-block:: python

    from solarnet_metadata.validation import validate_fits_keyword_data_type
    from solarnet_metadata.schema import SOLARNETSchema

    # Create a schema instance
    schema = SOLARNETSchema()

    # Example keyword and value
    keyword = "EXPTIME"
    value = 10.5

    # Validate the data type
    findings = validate_fits_keyword_data_type(
        keyword=keyword,
        value=value,
        schema=schema
    )
    
    if findings:
        print("Data type issues:")
        for finding in findings:
            print(finding)
