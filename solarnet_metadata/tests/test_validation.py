import pytest
from solarnet_metadata.validation import (
    validate_fits_keyword_value_comment,
    validate_fits_keyword_data_type,
)


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
        ("SOMEKEY", "val", None, []),
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
    findings = validate_fits_keyword_value_comment(keyword, value, comment)
    assert findings == expected_findings


# fmt: off
# Test cases for validate_fits_keyword_data_type
@pytest.mark.parametrize(
    "keyword,value,data_type,expected_findings",
    [
        # Valid integer
        ("SOMEKEY", "123", "int", []),
        # Invalid integer
        ("SOMEKEY", "abc", "int", ["Value for 'SOMEKEY' cannot be cast to data type 'int': invalid literal for int() with base 10: 'abc'"]),
        # Valid float
        ("SOMEKEY", "123.45", "float", []),
        # Invalid float
        ("SOMEKEY", "not a float", "float", ["Value for 'SOMEKEY' cannot be cast to data type 'float': could not convert string to float: 'not a float'"]),
        # Valid date (ISO format)
        ("SOMEKEY", "2023-01-01T00:00:00", "date", []),
        # Invalid date
        ("SOMEKEY", "invalid date", "date", ["Value for 'SOMEKEY' cannot be cast to data type 'date': Invalid isoformat string: 'invalid date'"]),
        # Boolean with non-empty string (passes since bool() succeeds)
        ("SOMEKEY", "any", "bool", []),
        # Boolean with empty string (passes since bool() succeeds)
        ("SOMEKEY", "", "bool", []),
        # Integer to string (passes since str() succeeds)
        ("SOMEKEY", 123, "str", []),
        # Unknown data type
        ("SOMEKEY", "value", "unknown", ["Unknown data type 'unknown' for keyword 'SOMEKEY'."]),
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
    ]
)
# fmt: on
def test_validate_fits_keyword_data_type(keyword, value, data_type, expected_findings):
    findings = validate_fits_keyword_data_type(keyword, value, data_type)
    assert findings == expected_findings
