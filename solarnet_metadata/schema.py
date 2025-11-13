"""
This module provides schema metadata templates an information.

"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import astropy.io.fits as fits
from astropy.table import Table

from solarnet_metadata import data_directory
from solarnet_metadata.util import DATA_TYPE_MAP, KeywordRequirement, load_yaml_data

logger = logging.getLogger(__name__)

__all__ = ["SOLARNETSchema"]

DEFAULT_ATTRS_SCHEMA_FILE = "SOLARNET_attr_schema.yaml"


class SOLARNETSchema:
    """
    Class representing a schema for SOLARNET requirements for solar observations.

    The SOLARNET Keyword information is loaded from YAML (dict-like) files in the following format:

    .. code-block:: yaml

        attribute_key:
            attribute_name:
                data_type: <string> # A string representing the data type of the attribute
                default: <Any> | null # A default value for the attribute of the given data type
                description: >
                    Include a meaningful description of the attribute and context needed to understand its values.
                human_readable: <string> # A human-readable version of the attribute name
                required: <bool> # Whether the attribute is required
                valid_values: optional[list] # A list of valid values for the attribute in the given data type
        conditional_requirements:
            - condition_type: <string> # The type of condition that must be met.
              condition_key: <string> # The keyword that the condition requirement is based on
              condition_value: optional[string] # The value that the condition requirement is based on.
              required_attributes: <list> # A list of keyword names that are required if the condition is met.

    Parameters
    ----------
    schema_layers :  `Optional[list[Path]]`
        Absolute file paths to attribute schema files. These schema files are layered
        on top of one another in a latest-priority ordering. That is, the latest file that modifies
        a common schema attribute will take precedence over earlier values for a given attribute.
    use_defaults: `Optional[bool]`
        Whether or not to load the default attribute schema files. These
        default schema files contain only the requirements for SOLARNET validation.

    Examples
    --------
    >>> from solarnet_metadata.schema import SOLARNETSchema
    >>> schema = SOLARNETSchema(use_defaults=True)
    >>> # Get Information about the AUTHOR Attriube
    >>> my_info = schema.attribute_info(attribute_name="AUTHOR")
    >>> # Get the template for required attributes
    >>> attribute_template = schema.attribute_template()
    """

    def __init__(
        self,
        schema_layers: Optional[list[Path]] = None,
        use_defaults: Optional[bool] = True,
    ):
        super().__init__()

        # Input Validation
        if not use_defaults and (schema_layers is None or len(schema_layers) == 0):
            raise ValueError(
                "Not enough information to create schema. You must either use the defaults or provide alternative layers for attribute schemas."
            )

        # Construct the Attribute Schema
        _attr_schema = {}
        if use_defaults:
            _def_attr_schema = self._load_default_attr_schema()
            _attr_schema = self._merge(
                base_layer=_attr_schema, new_layer=_def_attr_schema
            )
        if schema_layers is not None:
            # Merge each successive custom layer on top of the existing schema
            for schema_layer_path in schema_layers:
                attr_layer = load_yaml_data(yaml_file_path=schema_layer_path)
                _attr_schema = self._merge(
                    base_layer=_attr_schema, new_layer=attr_layer
                )
        # Set Final Member
        self._attr_schema = _attr_schema

        # Load Default Attributes
        self._default_attributes: fits.Header = self.load_default_attributes()

    @property
    def attribute_schema(self) -> Dict[str, Any]:
        """(`dict`) Schema for attributes of the file."""
        return self._attr_schema

    @property
    def attribute_key(self) -> Dict[str, Any]:
        """(`dict`) The attribute_key section of the schema."""
        return self._attr_schema.get("attribute_key", {})

    @property
    def default_attributes(self) -> fits.Header:
        """(`fits.Header`) Default Attributes applied for all Data Files"""
        return self._default_attributes

    def _load_default_attr_schema(self) -> dict:
        # The Default Schema file is contained in the `solarnet_metadata/data` directory
        default_schema_path = str(Path(data_directory) / DEFAULT_ATTRS_SCHEMA_FILE)
        # Load the Schema
        return load_yaml_data(yaml_file_path=default_schema_path)

    def load_default_attributes(self) -> fits.Header:
        """
        Function to load the default attributes for a SOLARNET-compliant data file.

        Returns
        -------
        header : `fits.Header`
            A FITS header containing the default attributes.
        """
        header = fits.Header()

        # Add Default Attributes to Header
        for keyword, info in self.attribute_key.items():
            if info.get("default", None) is None:
                # skip attributes without a default value
                continue

            # Try to cast the default value to the correct data type
            try:
                # NOTE PyYAML automatically converts ISO 8601 date strings to datetime objects
                # Additionally, fits.Header does not support datetime objects directly in cards
                # When we encounter a keyword a default value that is a datetime,
                # we convert it to an ISO 8601 string

                if isinstance(info["default"], datetime):
                    # Convert to ISO format string for FITS Header
                    value = info["default"].isoformat()
                else:
                    # Get the type conversion function - default to str if not found
                    type_converter = DATA_TYPE_MAP.get(info["data_type"], str)
                    # Convert the value using the appropriate function
                    value = type_converter(info["default"])

                # Add to Header with Comment
                header[keyword] = (
                    value,
                    self.get_comment(keyword),
                )
            except Exception as e:
                logger.warning(
                    f"Could not cast default value for {keyword} to {info['data_type']} was value {info['default']} with type {type(info['default'])}: FULL EXCEPTION: {e}"
                )
                # If we can't cast it, just use the raw value
                header[keyword] = (info["default"], self.get_comment(keyword))

        return header

    def get_required_keywords(
        self, primary: Optional[bool] = False, obs: Optional[bool] = False
    ) -> Dict[str, Dict[str, Any]]:
        """
        Function to get a list of required keywords based on whether the HDU is an observation HDU or not.

        Parameters
        ----------
        primary: `bool`, optional, default False
            Whether or not the HDU is a primary HDU. If True, the function will return
            keywords required for primary HDUs.
        obs: `bool`, optional, default False
            Whether or not the HDU is an observation HDU. If True, the function will return
            keywords required for observation HDUs.

        Returns
        -------
        required_keywords : `Dict[str, Dict[str, Any]]`
            A dictionary of required keywords and their associated information.
        """
        required_attributes = {
            keyword: info
            for keyword, info in self.attribute_key.items()
            if KeywordRequirement(info["required"]) == KeywordRequirement.ALL
            or (
                KeywordRequirement(info["required"]) == KeywordRequirement.PRIMARY
                and primary
            )
            or (KeywordRequirement(info["required"]) == KeywordRequirement.OBS and obs)
        }
        return required_attributes

    def get_optional_keywords(self) -> Dict[str, Dict[str, Any]]:
        """
        Function to get a list of optional keywords.

        Returns
        -------
        optional_keywords : `Dict[str, Dict[str, Any]]`
            A dictionary of optional keywords and their associated information.
        """
        optional_attributes = {
            keyword: info
            for keyword, info in self.attribute_key.items()
            if KeywordRequirement(info["required"]) == KeywordRequirement.OPTIONAL
        }
        return optional_attributes

    def attribute_template(
        self,
        primary: Optional[bool] = False,
        obs: Optional[bool] = False,
        observatory_type: Optional[str] = None,
        instrument_type: Optional[str] = None,
    ) -> fits.Header:
        """
        Function to generate a template of required attributes
        that must be set for a valid data file.

        Parameters
        ----------
        primary: `bool`, optional, default False
            Whether or not the template is being generated for a
            primary HDU. If True, the template will include attributes
            required for primary HDUs.]
        obs: `bool`, optional, default False
            Whether or not the template is being generated for an
            observation HDU. If True, the template will include
            attributes required for observation HDUs.
        observatory_type: `str`, optional, default None
            This details whether the observatory is `ground-based`,
            `earth-orbiting` or `deep-space` and can be used to determine
            the required metadata attributes for the observatory.
        instrument_type: `str`, optional, default None
            This details whether the instrument is `Imager` or `Spectrograph`
            and can be used to determine the required metadata attributes
            for the instrument.

        Returns
        -------
        template : `fits.Header`
            A template for required attributes that must be provided.
        """
        # Add Default Attributes to Header
        header = self.default_attributes.copy()

        # Add globally Required Attributes as BLANK keywords in header
        required_attributes = self.get_required_keywords(primary=primary, obs=obs)
        for keyword in required_attributes:
            header[keyword] = (header.get(keyword, None), self.get_comment(keyword))

        # Get required attributes for the conditional requirements based on observatory
        if (
            observatory_type
            and "OBS_TYPE" in self.attribute_key
            and observatory_type in self.attribute_key["OBS_TYPE"]["valid_values"]
        ):
            applicable_conditional_requirements: list[list[str]] = [
                requirement["required_attributes"]
                for requirement in self.attribute_schema["conditional_requirements"]
                if requirement["condition_key"] == "OBS_TYPE"
                and requirement["condition_value"] == observatory_type
            ]
            for conditional_requirement in applicable_conditional_requirements:
                for required_attribute in conditional_requirement:
                    header[required_attribute] = (
                        header.get(required_attribute, None),
                        self.get_comment(required_attribute),
                    )

        # Get required attributes for the conditional requirements based on instrument
        if (
            instrument_type
            and "INST_TYP" in self.attribute_key
            and instrument_type in self.attribute_key["INST_TYP"]["valid_values"]
        ):
            applicable_conditional_requirements: list[list[str]] = [
                requirement["required_attributes"]
                for requirement in self.attribute_schema["conditional_requirements"]
                if requirement["condition_key"] == "INST_TYP"
                and requirement["condition_value"] == instrument_type
            ]
            for conditional_requirement in applicable_conditional_requirements:
                for required_attribute in conditional_requirement:
                    header[required_attribute] = (
                        header.get(required_attribute, None),
                        self.get_comment(required_attribute),
                    )

        return header

    def attribute_info(self, attribute_name: Optional[str] = None):
        """
        Function to generate an `astropy.table.Table` of information about each
        metadata attribute. The Table contains all information in the SOLARNET attribute schema including:

        - attribute: (`str`) The name of the attribute
        - data_type: (`str`) The data type of the attribute
        - default: (`str`) The default value used if none is provided
        - description: (`str`) A description of the attribute and its context
        - human_readable: (`str`) A human-readable version of the attribute name
        - required: (`str`) Indicates the requirement level for the attribute. Possible values are:
            - 'all': required for all data
            - 'primary': required for primary data
            - 'obs': required for observational data
            - 'optional': not required, optional attribute
        - origin: (`str`) The origin of the attribute
        - valid_values: (`list`) A list of valid values for the attribute
        - pattern: (`str`) A regex pattern that the attribute value must match

        Parameters
        ----------
        attribute_name : `str`, optional, default None
            The name of the attribute to get specific information for.

        Returns
        -------
        info: `astropy.table.Table`
            A table of information about the SOLARNET keywords

        Raises
        ------
        KeyError: If attribute_name is not a recognized attribute.
        """

        # Strip the Description of New Lines
        for attr_name in self.attribute_key.keys():
            self.attribute_key[attr_name]["description"] = self.attribute_key[
                attr_name
            ]["description"].strip()

        # Create rows for the table
        rows = []
        for attr_name, attr_info in self.attribute_key.items():
            # Add the attribute name to the info dictionary
            row_data = {"Attribute": attr_name}
            row_data.update(attr_info)
            rows.append(row_data)

        # Create the Table
        info = Table(rows=rows)

        # Filter to specific attribute if requested
        if attribute_name is not None:
            mask = info["Attribute"] == attribute_name
            if not any(mask):
                raise KeyError(f"Cannot find attribute name: {attribute_name}")
            info = info[mask]

        return info

    def get_comment(self, attribute_name: str) -> Optional[str]:
        """
        Function to get the comment/description for a given attribute.

        Parameters
        ----------
        attribute_name : `str`
            The name of the attribute to get the comment for.

        Returns
        -------
        comment : `str` | `None`
            The comment/human-readable description for the attribute, or None if not found.
        """
        return self.attribute_key.get(attribute_name, {}).get("human_readable", None)

    def _merge(self, base_layer: dict, new_layer: dict, path: list = None) -> None:
        """
        Function to do in-place merging and updating of two dictionaries.
        This is an improvemnent over the built-in dict.update() method, as it allows for nested dictionaries and lists.

        Parameters
        ----------
        base_layer : `dict`
            The base dictionary to merge into.
        new_layer : `dict`
            The new dictionary to merge into the base.
        path : `list`
            The path to the current dictionary being merged. Used for recursion.

        Returns
        -------
        None - operation is done in-place.
        """
        # If we are at the top of the recursion, and we don't have a path, create a new one
        if not path:
            path = []
        # for each key in the base layer
        for key in new_layer:
            # If its a shared key
            if key in base_layer:
                # If both are dictionaries
                if isinstance(base_layer[key], dict) and isinstance(
                    new_layer[key], dict
                ):
                    # Merge the two nested dictionaries together
                    self._merge(base_layer[key], new_layer[key], path + [str(key)])
                # If both are lists
                elif isinstance(base_layer[key], list) and isinstance(
                    new_layer[key], list
                ):
                    # Extend the list of the base layer by the new layer
                    base_layer[key].extend(new_layer[key])
                # If they are not lists or dicts (scalars)
                elif base_layer[key] != new_layer[key]:
                    # We've reached a conflict, may want to overwrite the base with the new layer.
                    base_layer[key] = new_layer[key]
            # If its not a shared key
            else:
                base_layer[key] = new_layer[key]
        return base_layer
