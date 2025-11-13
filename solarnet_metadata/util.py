from datetime import datetime
from enum import Enum
from pathlib import Path

import yaml

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


def load_yaml_data(yaml_file_path: Path) -> dict:
    """
    Function to load data from a Yaml file.

    Parameters
    ----------
    yaml_file_path: `Path`
        Path to YAML file to be used for formatting.

    """
    if not Path(yaml_file_path).exists():
        raise FileNotFoundError(f"Cannot find YAML file: {yaml_file_path}")
    # Load the Yaml file to Dict
    yaml_data = {}
    with open(yaml_file_path, "r") as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data
