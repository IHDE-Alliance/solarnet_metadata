import pytest
from astropy.io import fits

from solarnet_metadata.schema import SOLARNETSchema
from solarnet_metadata.validation import (
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
    },
    "conditional_requirements": [],
}


# Helper function to create a SOLARNETSchema instance with mock schema
def create_mock_schema():
    schema = SOLARNETSchema()
    schema._attr_schema = MOCK_SCHEMA
    return schema


# Custom class to simulate a value that cannot be cast to a string
class BadStr:
    def __str__(self):
        raise ValueError("Cannot cast to string")


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
    ],
    ids=[
        "valid_regular_keyword",
        "invalid_keyword_too_long",
        "invalid_keyword_lowercase",
        "invalid_keyword_empty",
        "special_keyword_comment",
        "special_keyword_history",
        "integer_value",
        "card_exceeds_80_chars",
        "card_equals_80_chars",
        "value_not_castable_to_string",
        "comment_not_string",
        "comment_none",
    ]
)
# fmt: on
def test_validate_fits_keyword_value_comment(
    keyword, value, comment, expected_findings
):
    findings = validate_fits_keyword_value_comment(
        keyword, value, comment, warn_empty_keyword=True, warn_no_comment=True
    )
    assert findings == expected_findings


# fmt: off
# Test cases for validate_fits_keyword_data_type
@pytest.mark.parametrize(
    "keyword,value,data_type,expected_findings",
    [
        # Valid integer
        ("SOMEINT", "123", "int", []),
        # Invalid integer
        ("SOMEINT", "abc", "int", ["Value for 'SOMEINT' cannot be cast to data type 'int': invalid literal for int() with base 10: 'abc'"]),
        # Valid float
        ("SOMEFLOAT", "123.45", "float", []),
        # Invalid float
        ("SOMEFLOAT", "not a float", "float", ["Value for 'SOMEFLOAT' cannot be cast to data type 'float': could not convert string to float: 'not a float'"]),
        # Valid date (ISO format)
        ("SOMEDATE", "2023-01-01T00:00:00", "date", []),
        # Invalid date
        ("SOMEDATE", "invalid date", "date", ["Value for 'SOMEDATE' cannot be cast to data type 'date': Invalid isoformat string: 'invalid date'"]),
        # Boolean with non-empty string (passes since bool() succeeds)
        ("SOMEBOOL", "any", "bool", []),
        # Boolean with empty string (passes since bool() succeeds)
        ("SOMEBOOL", "", "bool", []),
        # Integer to string (passes since str() succeeds)
        ("SOMESTR", 123, "str", []),
        # Unknown data type
        ("SOMETYPE", "value", "unknown", ["Unknown data type 'unknown' for keyword 'SOMETYPE'."]),
        # Unknown Keyword
        ("SOMEKEY", "value", "unknown", ["Keyword 'SOMEKEY' not found in the schema. Cannot Validate Data Type."]),
    ],
    ids=[
        "valid_int",
        "invalid_int",
        "valid_float",
        "invalid_float",
        "valid_date",
        "invalid_date",
        "bool_non_empty_string",
        "bool_empty_string",
        "int_to_str",
        "unknown_data_type",
        "unknown_keyword",
    ]
)
# fmt: on
def test_validate_fits_keyword_data_type(keyword, value, data_type, expected_findings):
    schema = create_mock_schema()
    findings = validate_fits_keyword_data_type(keyword, value, schema)
    assert findings == expected_findings


# Parameterized test cases for the validate method
@pytest.mark.parametrize(
    "header_dict, warn_no_comment, warn_data_type, expected_findings",
    [
        # Test 1: Missing required attribute
        (
            {"NAXIS": ("3", "Number of axes")},
            False,
            False,
            ["Missing Required Attribute: AUTHOR"],
        ),
        # Test 2: Invalid keyword
        (
            {"NAXIS": ("3", "Number of axes"), "INVALID_KEY!": ("value", "comment")},
            False,
            False,
            [
                "Missing Required Attribute: AUTHOR",
                "Invalid keyword 'INVALID_KEY!': Must be 1-8 characters, containing only A-Z, 0-9, -, _.",
            ],
        ),
        # Test 3: Warn about missing comments
        (
            {"NAXIS": ("3", ""), "AUTHOR": ("John Doe", "")},
            True,
            False,
            [
                "Keyword 'NAXIS' has no comment.",
                "Keyword 'AUTHOR' has no comment.",
            ],
        ),
        # Test 4: Data type validation with correct types
        (
            {"NAXIS": ("3", "Number of axes"), "AUTHOR": ("John Doe", "Author name")},
            False,
            True,
            [],
        ),
        # Test 5: Data type validation with incorrect type
        (
            {
                "NAXIS": ("three", "Number of axes"),
                "AUTHOR": ("John Doe", "Author name"),
            },
            False,
            True,
            [
                "Value for 'NAXIS' cannot be cast to data type 'int': invalid literal for int() with base 10: 'three'",
            ],
        ),
        # Test 6: Keyword not in schema for data type validation
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "AUTHOR": ("John Doe", "Author name"),
                "EXTRAKEY": ("value", "comment"),
            },
            False,
            True,
            [
                "Keyword 'EXTRAKEY' not found in the schema. Cannot Validate Data Type.",
            ],
        ),
        # Test 7: Keyword in schema but without data_type
        (
            {
                "NAXIS": ("3", "Number of axes"),
                "AUTHOR": ("John Doe", "Author name"),
                "COMMENT": ("Test comment", "Comment description"),
            },
            False,
            True,
            [
                "Keyword 'COMMENT' has no data type. Cannot Validate Data Type.",
            ],
        ),
    ],
    ids=[
        "missing_required_attribute",
        "invalid_keyword",
        "warn_no_comment",
        "warn_data_type_correct",
        "warn_data_type_incorrect",
        "keyword_not_in_schema",
        "keyword_without_data_type",
    ],
)
def test_validate_header(
    header_dict, warn_no_comment, warn_data_type, expected_findings
):
    # Helper function to create a fits.Header from a dictionary of (value, comment) tuples
    def create_fits_header(header_dict):
        header = fits.Header()
        for key, (value, comment) in header_dict.items():
            header.set(key, value, comment)
        return header

    header = create_fits_header(header_dict)
    schema = create_mock_schema()
    findings = validate_header(
        header=header,
        warn_no_comment=warn_no_comment,
        warn_data_type=warn_data_type,
        schema=schema,
    )
    assert findings == expected_findings
