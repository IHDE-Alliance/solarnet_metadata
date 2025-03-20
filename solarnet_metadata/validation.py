import re
from typing import Any, List
from datetime import datetime

DATA_TYPE_MAP = {
    "bool": bool,
    "str": str,
    "int": int,
    "float": float,
    "date": datetime.fromisoformat,
}


def validate_fits_keyword_value_comment(
    keyword: str, value: Any, comment: str | None
) -> List[str]:
    """
    Validates a FITS keyword, value, and comment set according to FITS standard requirements.

    Parameters
    ----------
    keyword : str
        The FITS keyword to validate.
    value : Any
        The value associated with the keyword
    comment : str | None
        The comment associated with the keyword.

    Returns
    -------
    findings : List[str]
        A list of validation issues found; empty if the set is valid.
    """
    findings = []

    # Check keyword format: 1-8 characters, A-Z, 0-9, -, _
    if not isinstance(keyword, str) or not re.match(r"^[A-Z0-9_-]{1,8}$", keyword):
        findings.append(
            f"Invalid keyword '{keyword}': Must be 1-8 characters, containing only A-Z, 0-9, -, _."
        )

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
