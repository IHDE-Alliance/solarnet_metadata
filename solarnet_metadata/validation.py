from datetime import datetime
from enum import Enum
import re
from typing import Any, List, Optional

from astropy.io import fits

from solarnet_metadata.schema import SOLARNETSchema

DATA_TYPE_MAP = {
    "bool": bool,
    "str": str,
    "int": int,
    "float": float,
    "date": datetime.fromisoformat,
}


class KeywordRequirement(Enum):
    """
    Enum to represent the requirement level of a keyword in the FITS header.

    Valid values are:
    - `all`: The keyword is required for all HDUs.
    - `primary`: The keyword is required for the primary HDU only.
    - `obs`: Mandatory keywords for fully SOLARNET-compliant Obs-HDUs
    - `optional`: The keyword is optional and may be included in any HDU.
    """

    ALL = "all"
    PRIMARY = "primary"
    OBS = "obs"
    OPTIONAL = "optional"


def validate_header(
    header: fits.Header,
    is_primary: bool = False,
    is_obs: bool = False,
    warn_no_comment: bool = False,
    warn_data_type: bool = False,
    schema: Optional[SOLARNETSchema] = None,
) -> List[str]:
    """
    Validates a FITS header against the SOLARNET schema requirements.
    
    This function performs multiple validation checks:
    1. Verifies all required keywords are present based on HDU type
    2. Checks for pattern-based keywords when specified in the schema
    3. Validates each keyword, value, and comment according to FITS standards
    4. Optionally validates data types against the schema specifications
    
    Parameters
    ----------
    header : fits.Header
        The FITS header to validate.
    is_primary : bool, default False
        Whether this header belongs to a primary HDU, affecting which keywords are required.
    is_obs : bool, default False
        Whether this header belongs to an observation HDU, affecting which keywords are required.
    warn_no_comment : bool, default False
        Whether to report warnings for keywords missing comments.
    warn_data_type : bool, default False
        Whether to validate and report warnings about incorrect data types.
    schema : Optional[SOLARNETSchema], default None
        The schema to validate against. If None, the default SOLARNET schema is used.
    
    Returns
    -------
    validation_findings : List[str]
        A list of validation issues found; empty if the header is valid.
    """
    # Check if Custom Schema is provided
    if schema is None or not isinstance(schema, SOLARNETSchema):
        # Use the default schema
        schema = SOLARNETSchema()

    validation_findings = []

    # Get subset of Required Attributes
    required_attributes = {
        keyword: info
        for keyword, info in schema.attribute_schema["attribute_key"].items()
        if KeywordRequirement(info["required"]) == KeywordRequirement.ALL
        or (
            KeywordRequirement(info["required"]) == KeywordRequirement.PRIMARY
            and is_primary
        )
        or (KeywordRequirement(info["required"]) == KeywordRequirement.OBS and is_obs)
    }

    # Verify that all Required Attributes are present
    for keyword, info in required_attributes.items():
        if keyword not in header:
            # Check if there is a pattern match
            if pattern := info.get("pattern", None):
                found_match = False
                # See if anything in header matches the pattern
                for header_key in header.keys():
                    res = re.fullmatch(pattern, header_key)
                    if res:
                        # There was a match!
                        # print(f"Pattern match for {header_key} with pattern {pattern}")
                        found_match = True
                        break
                if not found_match:
                    validation_findings.append(
                        f"No pattern match for {keyword} with pattern {pattern}"
                    )
            else:
                validation_findings.append(f"Missing Required Attribute: {keyword}")

    for keyword, value, comment in header.cards:

        # Validate each keyword, value, comment set
        findings = validate_fits_keyword_value_comment(
            keyword, value, comment, warn_no_comment=warn_no_comment
        )
        validation_findings.extend(findings)

        # Placeholder for data type validation (extensible)
        if warn_data_type:
            # Make sure we have the keyword in the schema
            keyword_info = schema.attribute_schema["attribute_key"].get(keyword, None)
            if not keyword_info:
                validation_findings.append(
                    f"Keyword '{keyword}' not found in the schema. Cannot Validate Data Type."
                )
                continue
            # Make sure we have a data type for the keyword
            keyword_data_type = keyword_info.get("data_type", None)
            if not keyword_data_type:
                validation_findings.append(
                    f"Keyword '{keyword}' has no data type. Cannot Validate Data Type."
                )
            else:
                # check the data type of the keyword
                findings = validate_fits_keyword_data_type(
                    keyword=keyword,
                    value=value,
                    data_type=keyword_data_type,
                )
                validation_findings.extend(findings)

    return validation_findings


def validate_fits_keyword_value_comment(
    keyword: str,
    value: Any,
    comment: Optional[str] = None,
    warn_empty_keyword: bool = False,
    warn_no_comment: bool = False,
) -> List[str]:
    """
    Validates a FITS keyword, value, and comment set according to FITS standard requirements.
    
    This function checks:
    - Keyword format (1-8 characters, A-Z, 0-9, -, _)
    - Value string representation
    - Comment format
    - Total FITS card length (must be ≤80 characters)
    
    Special handling is applied for COMMENT and HISTORY keywords.

    Parameters
    ----------
    keyword : str
        The FITS keyword to validate.
    value : Any
        The value associated with the keyword.
    comment : Optional[str], default None
        The comment associated with the keyword.
    warn_empty_keyword : bool, default False
        Whether to add a warning if the keyword is empty.
    warn_no_comment : bool, default False
        Whether to add a warning if the comment is empty.

    Returns
    -------
    findings : List[str]
        A list of validation issues found; empty if the set is valid.
    """
    findings = []

    # Check for Empty Keyword
    if not keyword or keyword.strip() == "":
        if warn_empty_keyword:
            findings.append("Keyword is empty.")
    # Check keyword format: 1-8 characters, A-Z, 0-9, -, _
    elif not isinstance(keyword, str) or not re.match(r"^[A-Z0-9_-]{1,8}$", keyword):
        findings.append(
            f"Invalid keyword '{keyword}': Must be 1-8 characters, containing only A-Z, 0-9, -, _."
        )

    # Optional: Warn if comment is empty
    if warn_no_comment and (not comment or comment.strip() == ""):
        findings.append(f"Keyword '{keyword}' has no comment.")

    # Handle special keywords: COMMENT, HISTORY, and BLANK
    if keyword in ["COMMENT", "HISTORY"]:
        # We'll handle this later.
        pass  # TODO Special handling for COMMENT and HISTORY
    else:
        # For regular keywords, validate value and comment
        # Validate Value can be of any type, but must be able to be cast to a string
        value_str = None
        try:
            value_str = str(value)
        except Exception as e:
            findings.append(f"Value for '{keyword}' cannot be cast to a string: {e}")

        # Comment must be a string or None
        if comment is not None and not isinstance(comment, str):
            findings.append(
                f"Comment for '{keyword}' must be a string (got {type(comment)})."
            )
        elif (
            value_str is not None
        ):  # Only check length if value_str conversion succeeded
            # Simulate the FITS card: "KEYWORD = value / comment"
            # - Columns 1-8: keyword (padded to 8 with spaces)
            # - Column 9: '='
            # - Column 10: space
            # - Columns 11-80: value + ' / ' + comment (up to 70 characters total)
            card_str = f"{keyword.ljust(8)}= {value_str} / {comment}"
            if len(card_str) > 80:
                findings.append(
                    f"FITS card for '{keyword}' exceeds 80 characters (length: {len(card_str)})."
                )

    return findings


def validate_fits_keyword_data_type(
    keyword: str, value: Any, data_type: str
) -> List[str]:
    """
    Validates the data type of a FITS keyword value.

    Parameters
    ----------
    keyword : str
        The FITS keyword to validate.
    value : Any
        The value associated with the keyword.
    data_type : str
        The expected data type of the value.

    Returns
    -------
    findings : List[str]
        A list of validation issues found; empty if the data type is valid.
    """
    findings = []

    # Check if data type is known
    if data_type not in DATA_TYPE_MAP:
        findings.append(f"Unknown data type '{data_type}' for keyword '{keyword}'.")
        return findings

    # Check if value can be cast to the expected data type
    try:
        DATA_TYPE_MAP[data_type](value)
    except Exception as e:
        findings.append(
            f"Value for '{keyword}' cannot be cast to data type '{data_type}': {e}"
        )

    return findings
