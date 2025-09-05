from datetime import datetime
from enum import Enum

__all__ = ["DATA_TYPE_MAP", "KeywordRequirement"]


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
