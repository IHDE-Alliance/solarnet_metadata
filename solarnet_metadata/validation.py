import logging
import re
from pathlib import Path
from typing import Any, List, Optional, Tuple

from astropy.io import fits

from solarnet_metadata.schema import SOLARNETSchema
from solarnet_metadata.util import DATA_TYPE_MAP

logger = logging.getLogger(__name__)

__all__ = [
    "validate_file",
    "validate_header",
    "check_obs_hdu",
    "validate_fits_keyword_value_comment",
    "validate_fits_keyword_data_type",
]


def validate_file(
    file_path: Path,
    warn_empty_keyword: bool = False,
    warn_no_comment: bool = False,
    warn_data_type: bool = False,
    warn_missing_optional: bool = False,
    schema: Optional[SOLARNETSchema] = None,
) -> List[str]:
    """
    Validates a FITS file against the SOLARNET schema requirements.

    This function performs multiple validation checks:
    1. Verifies all required keywords are present based on HDU type
    2. Checks for pattern-based keywords when specified in the schema
    3. Validates each keyword, value, and comment according to FITS standards
    4. Optionally validates data types against the schema specifications

    Parameters
    ----------
    file_path : Path
        The path to the FITS file to validate.
    warn_empty_keyword : bool, default False
        Whether to report warnings for empty keywords.
    warn_no_comment : bool, default False
        Whether to report warnings for keywords missing comments.
    warn_data_type : bool, default False
        Whether to validate and report warnings about incorrect data types.
    warn_missing_optional : bool, default False
        Whether to report warnings for optional keywords that aren't included.
    schema : Optional[SOLARNETSchema], default None
        The schema to validate against. If None, the default SOLARNET schema is used.

    Returns
    -------
    validation_findings : List[str]
        A list of validation issues found; empty if the file is valid.
    """
    file_findings = []

    # Check if Custom Schema is provided
    if schema is None or not isinstance(schema, SOLARNETSchema):
        # Use the default schema
        schema = SOLARNETSchema()

    # Open the FITS file and get the header
    with fits.open(file_path) as hdul:
        primary_header = hdul[0].header

        # Validate primary header
        primary_findings = validate_header(
            primary_header,
            is_primary=True,
            warn_empty_keyword=warn_empty_keyword,
            warn_no_comment=warn_no_comment,
            warn_data_type=warn_data_type,
            warn_missing_optional=warn_missing_optional,
            schema=schema,
        )
        for finding in primary_findings:
            file_findings.append(f"Primary Header: {finding}")

        # Validate any additional observation headers
        for i in range(1, len(hdul)):
            findings = validate_header(
                hdul[i].header,
                is_primary=False,
                is_obs=True,
                warn_empty_keyword=warn_empty_keyword,
                warn_no_comment=warn_no_comment,
                warn_data_type=warn_data_type,
                warn_missing_optional=warn_missing_optional,
                schema=schema,
            )
            for finding in findings:
                file_findings.append(f"Observation Header {i}: {finding}")

    # Combine findings from both headers
    return file_findings


def validate_header(
    header: fits.Header,
    is_primary: bool = False,
    is_obs: bool = False,
    warn_empty_keyword: bool = False,
    warn_no_comment: bool = False,
    warn_data_type: bool = False,
    warn_missing_optional: bool = False,
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
    warn_empty_keyword : bool, default False
        Whether to report warnings for empty keywords.
    warn_no_comment : bool, default False
        Whether to report warnings for keywords missing comments.
    warn_data_type : bool, default False
        Whether to validate and report warnings about incorrect data types.
    warn_missing_optional : bool, default False
        Whether to report warnings for optional keywords that aren't included.
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

    # Initialize Empty List for Validation Findings
    validation_findings = []

    # Check Special Keyword for `OBS_HDU` which is an int, 0 or 1
    is_obs, obs_findings = check_obs_hdu(header, is_obs)
    validation_findings.extend(obs_findings)

    # Get subset of Required Attributes
    required_attributes = schema.get_required_keywords(primary=is_primary, obs=is_obs)
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
                        found_match = True
                        break
                if not found_match:
                    validation_findings.append(
                        f"Missing Required Attribute: {keyword}. No pattern match for {keyword} with pattern {pattern}"
                    )
            else:
                validation_findings.append(f"Missing Required Attribute: {keyword}")

    # Optionally Warn if Optional Attributes are missing
    if warn_missing_optional:
        optional_attributes = schema.get_optional_keywords()
        for keyword, info in optional_attributes.items():
            if keyword not in header:
                # Check if there is a pattern match
                if pattern := info.get("pattern", None):
                    found_match = False
                    # See if anything in header matches the pattern
                    for header_key in header.keys():
                        res = re.fullmatch(pattern, header_key)
                        if res:
                            # There was a match!
                            found_match = True
                            break
                    if not found_match:
                        validation_findings.append(
                            f"Missing Optional Attribute: {keyword}. No pattern match for {keyword} with pattern {pattern}"
                        )
                else:
                    validation_findings.append(f"Missing Optional Attribute: {keyword}")

    # Validate all of the existing keywords in the header
    for keyword, value, comment in header.cards:
        # Validate each keyword, value, comment set
        findings = validate_fits_keyword_value_comment(
            keyword,
            value,
            comment,
            warn_empty_keyword=warn_empty_keyword,
            warn_no_comment=warn_no_comment,
            schema=schema,
        )
        validation_findings.extend(findings)

        # Validate Date Type
        if warn_data_type and keyword and keyword.strip() != "":

            # check the data type of the keyword
            findings = validate_fits_keyword_data_type(
                keyword=keyword,
                value=value,
                schema=schema,
            )
            validation_findings.extend(findings)

    return validation_findings


def check_obs_hdu(header: fits.Header, is_obs: bool = False) -> Tuple[bool, List[str]]:
    """
    Check and validate the OBS_HDU keyword in a FITS header.

    This function validates whether a header contains a properly formatted OBS_HDU
    keyword (with value 0 or 1) and reconciles any discrepancies between the header
    value and the provided is_obs parameter.

    Parameters
    ----------
    header : fits.Header
        The FITS header to check for OBS_HDU keyword.
    is_obs : bool, default False
        Initial assumption about whether this is an observation HDU.

    Returns
    -------
    is_obs : bool
        The resolved observation HDU status, potentially modified based on the
        header's OBS_HDU value.
    validation_findings : List[str]
        A list of validation issues found; empty if OBS_HDU is valid.

    Notes
    -----
    If there are discrepancies between the provided is_obs parameter and the
    header's OBS_HDU value, this function will override is_obs to match the
    header and log appropriate warnings.
    """
    validation_findings = []
    if "OBS_HDU" in header:
        if header["OBS_HDU"] not in [0, 1]:
            validation_findings.append(
                f"Invalid OBS_HDU value: {header['OBS_HDU']}. Must be 0 or 1."
            )
            is_obs = False
        if header["OBS_HDU"] == 1 and not is_obs:
            logger.warning(
                f"Keyword `OBS_HDU` is set to 1, but `is_obs` given as False. Overriding `is_obs` to True. If this is not the desired behavior, please check the header `OBS_HDU`."
            )
            is_obs = True
        elif header["OBS_HDU"] == 0 and is_obs:
            logger.warning(
                f"Keyword `OBS_HDU` is set to 0, but `is_obs` given as True. Overriding `is_obs` to False. If this is not the desired behavior, please check the header `OBS_HDU`."
            )
            is_obs = False
    elif "OBS_HDU" not in header and is_obs:
        logger.warning(
            f"Keyword `OBS_HDU` is not present in the header, but `is_obs` given as True. Overriding `is_obs` to True. If this is not the desired behavior, please check the header `OBS_HDU`."
        )
        is_obs = True
    return is_obs, validation_findings


def validate_fits_keyword_value_comment(
    keyword: str,
    value: Any,
    comment: Optional[str] = None,
    warn_empty_keyword: bool = False,
    warn_no_comment: bool = False,
    schema: Optional[SOLARNETSchema] = None,
) -> List[str]:
    """
    Validates a FITS keyword, value, and comment set according to FITS standard requirements.

    This function checks:
    - Keyword format (1-8 characters, A-Z, 0-9, -, _)
    - Value string representation
    - Comment format
    - Total FITS card length (must be ≤80 characters)
    - Valid values of the keyword if specified in the schema

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
    schema : Optional[SOLARNETSchema], default None
        The schema to validate against. If None, the default SOLARNET schema is used.

    Returns
    -------
    findings : List[str]
        A list of validation issues found; empty if the set is valid.
    """

    # Check if Custom Schema is provided
    if schema is None or not isinstance(schema, SOLARNETSchema):
        # Use the default schema
        schema = SOLARNETSchema()

    # Initialize Empty List for Findings
    findings = []

    # Check for Empty Keyword
    if not keyword or keyword.strip() == "":
        if warn_empty_keyword:
            findings.append(
                f"Invalid keyword '{keyword}': Must be 1-8 characters, containing only A-Z, 0-9, -, _."
            )
    # Check keyword format: 1-8 characters, A-Z, 0-9, -, _
    elif not isinstance(keyword, str) or not re.match(r"^[A-Z0-9_-]{1,8}$", keyword):
        findings.append(
            f"Invalid keyword '{keyword}': Must be 1-8 characters, containing only A-Z, 0-9, -, _."
        )

    # Optional: Warn if comment is empty
    if warn_no_comment and (not comment or str(comment).strip() == ""):
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

    # Check for Valid Values in the Schema
    attribute_key = schema.attribute_key
    if keyword in attribute_key:
        valid_values = attribute_key[keyword].get("valid_values", None)
        if valid_values and value not in valid_values:
            findings.append(
                f"Value '{value}' for keyword '{keyword}' is not in the list of valid values: {valid_values}."
            )

    return findings


def validate_fits_keyword_data_type(
    keyword: str,
    value: Any,
    schema: Optional[SOLARNETSchema] = None,
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
    # Check if Custom Schema is provided
    if schema is None or not isinstance(schema, SOLARNETSchema):
        # Use the default schema
        schema = SOLARNETSchema()

    findings = []

    # Check if the keyword is in the schema
    keyword_info = schema.attribute_key.get(keyword, None)
    if not keyword_info:
        # Search for Pattern Match in the Schema
        found_match = False
        for _, info in schema.attribute_key.items():
            if pattern := info.get("pattern", None):
                res = re.fullmatch(pattern, keyword)
                if res:
                    found_match = True
                    keyword_info = info
                    break
        if not found_match:
            findings.append(
                f"Keyword '{keyword}' not found in the schema. Cannot Validate Data Type."
            )

    if keyword_info:
        # Make sure we have a data type for the keyword
        data_type = keyword_info.get("data_type", None)
        if not data_type:
            findings.append(
                f"Keyword '{keyword}' has no data type. Cannot Validate Data Type."
            )
        # Check if data type is known
        elif data_type not in DATA_TYPE_MAP:
            findings.append(f"Unknown data type '{data_type}' for keyword '{keyword}'.")
            return findings
        else:
            # Check if value can be cast to the expected data type
            try:
                DATA_TYPE_MAP[data_type](value)
            except Exception as e:
                findings.append(
                    f"Value for '{keyword}' cannot be cast to data type '{data_type}': {e}"
                )

    return findings
