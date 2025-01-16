"""
This module provides schema metadata templates an information.

"""

from pathlib import Path
from typing import Optional
import yaml

import solarnet_metadata

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
            for schema_layer_path in schema_layers:
                attr_layer = self._load_yaml_data(yaml_file_path=schema_layer_path)
                _attr_schema = self._merge(
                    base_layer=_attr_schema, new_layer=attr_layer
                )
        # Set Final Member
        self._attr_schema = _attr_schema

        # Load Default Attributes
        self._default_attributes = self._load_default_attributes(
            schema=self._attr_schema
        )

    @property
    def attribute_schema(self):
        """(`dict`) Schema for attributes of the file."""
        return self._attr_schema

    @property
    def default_attributes(self):
        """(`dict`) Default Attributes applied for all Data Files"""
        return self._default_attributes

    def _load_default_attr_schema(self) -> dict:
        # The Default Schema file is contained in the `solarnet_metadata/data` directory
        default_schema_path = str(
            Path(solarnet_metadata.__file__).parent / "data" / DEFAULT_ATTRS_SCHEMA_FILE
        )
        # Load the Schema
        return self._load_yaml_data(yaml_file_path=default_schema_path)

    def _load_default_attributes(self, schema: dict) -> dict:
        return {
            attr_name: info["default"]
            for attr_name, info in schema["attribute_key"].items()
            if info["default"] is not None
        }

    def _load_yaml_data(self, yaml_file_path: Path) -> dict:
        """
        Function to load data from a Yaml file.

        Parameters
        ----------
        yaml_file_path: `Path`
            Path to schema file to be used for formatting.

        """
        assert Path(yaml_file_path).exists()
        # Load the Yaml file to Dict
        yaml_data = {}
        with open(yaml_file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data

    def attribute_template(
        self,
        observatory_type: Optional[str] = None,
        instrument_type: Optional[str] = None,
    ) -> dict:
        """
        Function to generate a template of required attributes
        that must be set for a valid data file.

        Parameters
        ----------
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
        template : `dict`
            A template for required attributes that must be provided.
        """
        template = {}
        for attr_name, attr_schema in self.attribute_schema["attribute_key"].items():
            if attr_schema["required"] and attr_name not in self.default_attributes:
                template[attr_name] = None

        # Get required attributes for the conditional requirements based on observatory
        if (
            observatory_type
            and observatory_type
            in self.attribute_schema["attribute_key"]["OBS_TYPE"]["valid_values"]
        ):
            applicable_conditional_requirements: list[list[str]] = [
                requirement["required_attributes"]
                for requirement in self.attribute_schema["conditional_requirements"]
                if requirement["condition_key"] == "OBS_TYPE"
                and requirement["condition_value"] == observatory_type
            ]
            for conditional_requirement in applicable_conditional_requirements:
                for required_attribute in conditional_requirement:
                    template[required_attribute] = None

        # Get required attributes for the conditional requirements based on instrument
        if (
            instrument_type
            and instrument_type
            in self.attribute_schema["attribute_key"]["INST_TYP"]["valid_values"]
        ):
            applicable_conditional_requirements: list[list[str]] = [
                requirement["required_attributes"]
                for requirement in self.attribute_schema["conditional_requirements"]
                if requirement["condition_key"] == "INST_TYP"
                and requirement["condition_value"] == instrument_type
            ]
            for conditional_requirement in applicable_conditional_requirements:
                for required_attribute in conditional_requirement:
                    template[required_attribute] = None

        return template

    def attribute_info(self, attribute_name: Optional[str] = None):
        """
        Function to generate a `pd.DataFrame` of information about each
        metadata attribute. The `pd.DataFrame` contains all information in the SOLARNET attribute schema including:

        - description: (`str`) A brief description of the attribute
        - default: (`str`) The default value used if none is provided
        - required: (`bool`) Whether the attribute is required by SWxSOC standards


        Parameters
        ----------
        attribute_name : `str`, optional, default None
            The name of the attribute to get specific information for.

        Returns
        -------
        info: `pd.DataFrame`
            A table of information about the SOLARNET keywords

        Raises
        ------
        KeyError: If attribute_name is not a recognized attribute.
        """
        import pandas as pd

        attribute_key = self.attribute_schema["attribute_key"]

        # Strip the Description of New Lines
        for attr_name in attribute_key.keys():
            attribute_key[attr_name]["description"] = attribute_key[attr_name][
                "description"
            ].strip()

        # Create the Info Table
        info = pd.DataFrame.from_dict(attribute_key, orient="index")
        # Reset the Index, add Attribute as new column
        info.reset_index(names="Attribute", inplace=True)

        # Limit the Info to the requested Attribute
        if attribute_name and attribute_name in info["Attribute"].values:
            info = info[info["Attribute"] == attribute_name]
        elif attribute_name and attribute_name not in info["Attribute"].values:
            raise KeyError(f"Cannot find attribute name: {attribute_name}")

        return info

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
