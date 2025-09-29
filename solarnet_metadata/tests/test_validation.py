import logging
import tempfile
from pathlib import Path

import pytest
from astropy.io import fits

from solarnet_metadata.schema import SOLARNETSchema
from solarnet_metadata.validation import (
    check_obs_hdu,
    validate_file,
    validate_fits_keyword_data_type,
    validate_fits_keyword_value_comment,
    validate_header,
)

# Mock schema for testing
MOCK_SCHEMA = {
    "attribute_key": {
        "NAXIS": {"required": "obs", "data_type": "int"},
        "COMMENT": {"required": "optional"},
        "AUTHOR": {"required": "all", "data_type": "str"},
        "SOMEINT": {"required": "optional", "data_type": "int"},
        "SOMEFLOAT": {"required": "optional", "data_type": "float"},
        "SOMEDATE": {"required": "optional", "data_type": "date"},
        "SOMESTR": {"required": "optional", "data_type": "str"},
        "SOMEBOOL": {"required": "optional", "data_type": "bool"},
        "SOMETYPE": {"required": "optional", "data_type": "unknown"},
        "VALIDKEY": {
            "required": "optional",
            "data_type": "str",
            "valid_values": ["A", "B", "C"],
        },
        "PATTERNn": {
            "required": "all",
            "data_type": "str",
            "pattern": "PATTERN(?P<n>[1-9])",
        },
        "OBS_ATTR": {"required": "obs", "data_type": "str"},
        "OPT_PTRn": {
            "required": "optional",
            "data_type": "str",
            "pattern": "OPT_PTR(?P<n>[1-9])",
        },
    },
    "conditional_requirements": [],
}


@pytest.fixture
def mock_schema():
    schema = SOLARNETSchema()
    schema._attr_schema = MOCK_SCHEMA
    schema._default_attributes = schema.load_default_attributes
    return schema


# Custom class to simulate a value that cannot be cast to a string
class BadStr:
    def __str__(self):
        raise ValueError("Cannot cast to string")


@pytest.fixture
def header_without_obs_hdu():
    """Create a FITS header without OBS_HDU keyword."""
    header = fits.Header()
    header["SIMPLE"] = True
    header["NAXIS"] = 0
    return header


@pytest.fixture
def header_with_obs_hdu_0():
    """Create a FITS header with OBS_HDU=0."""
    header = fits.Header()
    header["SIMPLE"] = True
    header["NAXIS"] = 0
    header["OBS_HDU"] = 0
    return header


@pytest.fixture
def header_with_obs_hdu_1():
    """Create a FITS header with OBS_HDU=1."""
    header = fits.Header()
    header["SIMPLE"] = True
    header["NAXIS"] = 0
    header["OBS_HDU"] = 1
    return header


@pytest.fixture
def header_with_invalid_obs_hdu():
    """Create a FITS header with invalid OBS_HDU value."""
    header = fits.Header()
    header["SIMPLE"] = True
    header["NAXIS"] = 0
    header["OBS_HDU"] = 2  # Invalid value, should be 0 or 1
    return header


@pytest.mark.parametrize(
    "header_fixture, is_obs_input, expected_is_obs, expected_findings, should_log",
    [
        # OBS_HDU not in header
        ("header_without_obs_hdu", False, False, [], False),  # Default case
        ("header_without_obs_hdu", True, True, [], True),  # Warning case
        # OBS_HDU=0 in header
        ("header_with_obs_hdu_0", False, False, [], False),  # Matching case
        ("header_with_obs_hdu_0", True, False, [], True),  # Override case
        # OBS_HDU=1 in header
        ("header_with_obs_hdu_1", False, True, [], True),  # Override case
        ("header_with_obs_hdu_1", True, True, [], False),  # Matching case
        # Invalid OBS_HDU in header
        (
            "header_with_invalid_obs_hdu",
            False,
            False,
            ["Invalid OBS_HDU value: 2. Must be 0 or 1."],
            False,
        ),
        (
            "header_with_invalid_obs_hdu",
            True,
            False,
            ["Invalid OBS_HDU value: 2. Must be 0 or 1."],
            False,
        ),
    ],
)
def test_check_obs_hdu(
    header_fixture,
    is_obs_input,
    expected_is_obs,
    expected_findings,
    should_log,
    request,
    caplog,
):
    """Test check_obs_hdu function with various scenarios."""
    # Get the header fixture
    header = request.getfixturevalue(header_fixture)

    # Set log level to capture warnings
    caplog.set_level(logging.WARNING)

    # Call the function
    result_is_obs, result_findings = check_obs_hdu(header, is_obs_input)

    # Check return values
    assert result_is_obs == expected_is_obs
    assert result_findings == expected_findings

    # Check if warning was logged when expected
    if should_log:
        assert len(caplog.records) > 0
        assert any("Overriding `is_obs`" in record.message for record in caplog.records)
    else:
        # Either no logs or only validation findings (not warnings about overriding)
        assert all(
            "Overriding `is_obs`" not in record.message for record in caplog.records
        )


# fmt: off
# Test cases for validate_fits_keyword_value_comment
@pytest.mark.parametrize(
    "keyword,value,comment,expected_findings",
    [
        # Valid case: regular keyword, string value, string comment
        ("NAXIS", "3", "Number of axes", []),
        # Invalid keyword: too long
        ("TOOLONGKEYWORD", "value", "comment", ["Invalid keyword 'TOOLONGKEYWORD': Must be 1-8 characters, containing only A-Z, 0-9, -, _."]),
        # Invalid keyword: contains lowercase letters
        ("lower_case", "value", "comment", ["Invalid keyword 'lower_case': Must be 1-8 characters, containing only A-Z, 0-9, -, _."]),
        # Invalid keyword: empty string
        ("", "value", "comment", ["Invalid keyword '': Must be 1-8 characters, containing only A-Z, 0-9, -, _."]),
        # Special keyword COMMENT: currently passes regardless of value/comment
        ("COMMENT", "", "This is a comment", []),
        # Special keyword HISTORY: currently passes regardless of value/comment
        ("HISTORY", None, "History entry", []),
        # Regular keyword with integer value (castable to string)
        ("SOMEKEY", 123, "comment", []),
        # FITS card exceeds 80 characters
        ("SOMEKEY", "a" * 30, "b" * 38, ["FITS card for 'SOMEKEY' exceeds 80 characters (length: 81)."]),
        # FITS card exactly 80 characters (should pass)
        ("SOMEKEY", "a" * 30, "b" * 37, []),
        # Value cannot be cast to string
        ("SOMEKEY", BadStr(), "comment", ["Value for 'SOMEKEY' cannot be cast to a string: Cannot cast to string"]),
        # Comment is not a string or None
        ("SOMEKEY", "value", 123, ["Comment for 'SOMEKEY' must be a string (got <class 'int'>)."]),
        # Comment is None (should pass, though FITS card includes " / None")
        ("SOMEKEY", "val", None, ["Keyword 'SOMEKEY' has no comment."]),
        # Keyword with Value outside valid_values
        ("VALIDKEY", "D", "comment", ["Value 'D' for keyword 'VALIDKEY' is not in the list of valid values: ['A', 'B', 'C']."]),
    ]
)
# fmt: on
def test_validate_fits_keyword_value_comment(
    mock_schema, keyword, value, comment, expected_findings
):
    findings = validate_fits_keyword_value_comment(
        keyword,
        value,
        comment,
        warn_empty_keyword=True,
        warn_no_comment=True,
        schema=mock_schema,
    )
    assert findings == expected_findings


# fmt: off
# Test cases for validate_fits_keyword_data_type
@pytest.mark.parametrize(
    "keyword,value,expected_findings",
    [
        # Valid integer
        ("SOMEINT", "123", []),
        # Invalid integer
        ("SOMEINT", "abc", ["Value for 'SOMEINT' cannot be cast to data type 'int': invalid literal for int() with base 10: 'abc'"]),
        # Valid float
        ("SOMEFLOAT", "123.45", []),
        # Invalid float
        ("SOMEFLOAT", "not a float", ["Value for 'SOMEFLOAT' cannot be cast to data type 'float': could not convert string to float: 'not a float'"]),
        # Valid date (ISO format)
        ("SOMEDATE", "2023-01-01T00:00:00", []),
        # Invalid date
        ("SOMEDATE", "invalid date", ["Value for 'SOMEDATE' cannot be cast to data type 'date': Invalid isoformat string: 'invalid date'"]),
        # Boolean with non-empty string (passes since bool() succeeds)
        ("SOMEBOOL", "any", []),
        # Boolean with empty string (passes since bool() succeeds)
        ("SOMEBOOL", "", []),
        # Integer to string (passes since str() succeeds)
        ("SOMESTR", 123, []),
        # Unknown data type
        ("SOMETYPE", "value", ["Unknown data type 'unknown' for keyword 'SOMETYPE'."]),
        # Unknown Keyword
        ("SOMEKEY", "value", ["Keyword 'SOMEKEY' not found in the schema. Cannot Validate Data Type."]),
        # PATTERN matching keyword
        ("PATTERN1", "value", []),
    ]
)
# fmt: on
def test_validate_fits_keyword_data_type(
    mock_schema, keyword, value, expected_findings
):
    findings = validate_fits_keyword_data_type(
        keyword=keyword, value=value, schema=mock_schema
    )
    assert findings == expected_findings


@pytest.mark.parametrize(
    "header_dict, warn_no_comment, warn_data_type, warn_missing_optional, expected_findings",
    [
        # Test 1: Missing required attribute
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
            },
            False,
            False,
            False,
            ["Missing Required Attribute: AUTHOR"],
        ),
        # Test 2: Invalid keyword
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "INVALID_KEY!": ("value", "comment"),
            },
            False,
            False,
            False,
            [
                "Missing Required Attribute: AUTHOR",
                "Invalid keyword 'INVALID_KEY!': Must be 1-8 characters, containing only A-Z, 0-9, -, _.",
            ],
        ),
        # Test 3: Warn about missing comments
        (
            {
                "NAXIS": ("3", ""),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", ""),
            },
            True,
            False,
            False,
            [
                "Keyword 'NAXIS' has no comment.",
                "Keyword 'AUTHOR' has no comment.",
            ],
        ),
        # Test 4: Data type validation with correct types
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
            },
            False,
            True,
            False,
            [],
        ),
        # Test 5: Data type validation with incorrect type
        (
            {
                "NAXIS": ("three", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
            },
            False,
            True,
            False,
            [
                "Value for 'NAXIS' cannot be cast to data type 'int': invalid literal for int() with base 10: 'three'",
            ],
        ),
        # Test 6: Keyword not in schema for data type validation
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
                "EXTRAKEY": ("value", "comment"),
            },
            False,
            True,
            False,
            [
                "Keyword 'EXTRAKEY' not found in the schema. Cannot Validate Data Type.",
            ],
        ),
        # Test 7: Keyword in schema but without data_type
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
                "COMMENT": ("Test comment", "Comment description"),
            },
            False,
            True,
            False,
            [
                "Keyword 'COMMENT' has no data type. Cannot Validate Data Type.",
            ],
        ),
        # Test 8: Valid keyword with value outside valid_values
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
                "VALIDKEY": ("D", "Invalid value"),
            },
            False,
            True,
            False,
            [
                "Value 'D' for keyword 'VALIDKEY' is not in the list of valid values: ['A', 'B', 'C'].",
            ],
        ),
        # Test 9: Pattern matching keyword not found in schema
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "AUTHOR": ("John Doe", "Author name"),
            },
            False,
            True,
            False,
            [
                "Missing Required Attribute: PATTERNn. No pattern match for PATTERNn with pattern PATTERN(?P<n>[1-9])",
            ],
        ),
        # Test 10: Missing optional pattern-matching keywords with warn_missing_optional=True
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
                # Only one optional keyword present
                "COMMENT": ("Test comment", "Comment description"),
                # No optional pattern keywords
            },
            False,
            False,
            True,  # warn_missing_optional
            [
                "Missing Optional Attribute: SOMEINT",
                "Missing Optional Attribute: SOMEFLOAT",
                "Missing Optional Attribute: SOMEDATE",
                "Missing Optional Attribute: SOMESTR",
                "Missing Optional Attribute: SOMEBOOL",
                "Missing Optional Attribute: SOMETYPE",
                "Missing Optional Attribute: VALIDKEY",
                "Missing Optional Attribute: OPT_PTRn. No pattern match for OPT_PTRn with pattern OPT_PTR(?P<n>[1-9])",
            ],
        ),
        # Test 11: Pattern-matching optional keyword is present
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "PATTERN1": ("value", "comment"),
                "AUTHOR": ("John Doe", "Author name"),
                "OPT_PTR1": ("value", "Optional pattern value"),
                # One optional pattern keyword present
            },
            False,
            False,
            True,  # warn_missing_optional
            [
                "Missing Optional Attribute: COMMENT",
                "Missing Optional Attribute: SOMEINT",
                "Missing Optional Attribute: SOMEFLOAT",
                "Missing Optional Attribute: SOMEDATE",
                "Missing Optional Attribute: SOMESTR",
                "Missing Optional Attribute: SOMEBOOL",
                "Missing Optional Attribute: SOMETYPE",
                "Missing Optional Attribute: VALIDKEY",
                # No warning for OPT_PTRn since OPT_PTR1 is present
            ],
        ),
    ],
)
def test_validate_header(
    mock_schema,
    header_dict,
    warn_no_comment,
    warn_data_type,
    warn_missing_optional,
    expected_findings,
):
    # Helper function to create a fits.Header from a dictionary of (value, comment) tuples
    def create_fits_header(header_dict):
        header = fits.Header()
        for key, (value, comment) in header_dict.items():
            header.set(key, value, comment)
        return header

    header = create_fits_header(header_dict)
    findings = validate_header(
        header=header,
        warn_no_comment=warn_no_comment,
        warn_data_type=warn_data_type,
        warn_missing_optional=warn_missing_optional,
        schema=mock_schema,
    )
    assert findings == expected_findings


def create_test_fits_file(primary_header_dict, data_headers_list=None, filepath=None):
    """Create a test FITS file with specified headers."""
    # Create primary HDU
    primary_hdu = fits.PrimaryHDU()
    for key, (value, comment) in primary_header_dict.items():
        primary_hdu.header[key] = (value, comment)

    # Create HDU list
    hdul = fits.HDUList([primary_hdu])

    # Add data HDUs if provided
    if data_headers_list:
        for header_dict in data_headers_list:
            data_hdu = fits.ImageHDU()
            for key, (value, comment) in header_dict.items():
                data_hdu.header[key] = (value, comment)
            hdul.append(data_hdu)

    # Write to file
    hdul.writeto(filepath, overwrite=True)
    return filepath


@pytest.mark.parametrize(
    "primary_header, data_headers, warn_params, expected_patterns",
    [
        # Test case 1: Valid file with all required keywords
        (
            {
                "AUTHOR": ("Test Author", "Author name"),
                "PATTERN1": ("Value", "Pattern match"),
            },
            None,
            (False, False, False),  # (warn_empty, warn_comment, warn_data_type)
            [],  # No findings expected
        ),
        # Test case 2: Missing required keyword in primary header
        (
            {
                "PATTERN1": ("Value", "Pattern match"),
                # Missing AUTHOR
            },
            None,
            (False, False, False),
            ["Primary Header: Missing Required Attribute: AUTHOR"],
        ),
        # Test case 3: File with valid observation HDU
        (
            {
                "AUTHOR": ("Test Author", "Author name"),
                "PATTERN1": ("Value", "Pattern match"),
            },
            [
                {
                    "OBS_HDU": (1, "Observation HDU flag"),
                    "NAXIS": (2, "Number of axes"),
                    "AUTHOR": ("Test Author", "Author name"),
                    "PATTERN1": ("Value", "Pattern match"),
                    "OBS_ATTR": ("Obs Value", "Observation attribute"),
                }
            ],
            (False, False, False),
            [],  # No findings expected
        ),
        # Test case 4: Error in observation HDU
        (
            {
                "AUTHOR": ("Test Author", "Author name"),
                "PATTERN1": ("Value", "Pattern match"),
            },
            [
                {
                    "OBS_HDU": (1, "Observation HDU flag"),
                    # Missing OBS_ATTR in observation HDU
                    "AUTHOR": ("Test Author", "Author name"),
                    "PATTERN1": ("Value", "Pattern match"),
                }
            ],
            (False, False, False),
            ["Observation Header 1: Missing Required Attribute: OBS_ATTR"],
        ),
        # Test case 5: Multiple HDUs with issues
        (
            {
                "AUTHOR": ("Test Author", "Author name"),
                "PATTERN1": ("Value", "Pattern match"),
            },
            [
                {
                    "OBS_HDU": (1, "Observation HDU flag"),
                    "NAXIS": (2, "Number of axes"),
                    "AUTHOR": ("Test Author", "Author name"),
                    "PATTERN1": ("Value", "Pattern match"),
                    "OBS_ATTR": ("Obs Value", "Observation attribute"),
                },
                {
                    "OBS_HDU": (1, "Observation HDU flag"),
                    # Missing OBS_ATTR
                    "AUTHOR": ("Test Author", "Author name"),
                    "PATTERN1": ("Value", "Pattern match"),
                },
            ],
            (False, False, False),
            ["Observation Header 2: Missing Required Attribute: OBS_ATTR"],
        ),
    ],
)
def test_validate_file(
    mock_schema, primary_header, data_headers, warn_params, expected_patterns
):
    """Test the validate_file function with different file configurations."""
    # Create a temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "test_file.fits"
        # Create a test FITS file
        filepath = create_test_fits_file(
            primary_header, data_headers, filepath=temp_file
        )

        # Unpack warning parameters
        warn_empty, warn_comment, warn_data_type = warn_params

        # Validate the file
        findings = validate_file(
            Path(filepath),
            warn_empty_keyword=warn_empty,
            warn_no_comment=warn_comment,
            warn_data_type=warn_data_type,
            schema=mock_schema,
        )

        # Check for expected findings patterns
        if not expected_patterns:
            assert not findings, f"Expected no findings but got: {findings}"
        else:
            for pattern in expected_patterns:
                assert any(
                    pattern in finding for finding in findings
                ), f"Pattern '{pattern}' not found in findings: {findings}"
