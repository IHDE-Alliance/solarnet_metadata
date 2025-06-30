import tempfile
from pathlib import Path

import pandas as pd
import pytest
import yaml

from solarnet_metadata.schema import SOLARNETSchema


def test_schema_default():
    """Test Creating a Schema with Default Parameters"""
    schema = SOLARNETSchema()

    # Attribute Schema
    assert schema.attribute_schema is not None
    assert isinstance(schema.attribute_schema, dict)

    # Default Attributes
    assert schema.default_attributes is not None
    assert isinstance(schema.default_attributes, dict)

    # Attribute Template
    assert schema.attribute_template() is not None
    assert isinstance(schema.attribute_template(), dict)

    # Attribute Template with specified conditionals
    template = schema.attribute_template(
        observatory_type="ground-based", instrument_type="Spectrograph"
    )
    assert template is not None
    assert isinstance(template, dict)
    # Assert conditional requirements are present
    assert "OBSGEO-X" in template
    assert "OBSGEO-Y" in template
    assert "OBSGEO-Z" in template
    assert "SPECSYS" in template

    # Attribute Info
    assert schema.attribute_info() is not None
    assert isinstance(schema.attribute_info(), pd.DataFrame)
    assert isinstance(schema.attribute_info(attribute_name="AUTHOR"), pd.DataFrame)
    with pytest.raises(KeyError):
        _ = schema.attribute_info(attribute_name="NotAnAttribute")


def test_sw_schema_invalid_params():
    """Test Creating a Schema with Invalid Parameters"""
    with pytest.raises(ValueError):
        _ = SOLARNETSchema(schema_layers=None, use_defaults=None)


def test_sw_schema_custom_layers():
    """Test Creating a Schema with Custom Layers"""
    with tempfile.TemporaryDirectory() as tmpdirname:

        # Create Extra Layer for Testing
        layer_content = """
        attribute_key:
            test_attribute:
                description: This is a test attribute
                default: null
                required: true
                valid_values: null
            AUTHOR:
                description: Author
                default: null
                required: false   # originally required in Default Schema
        """

        test_path = Path(tmpdirname) / "layer_test.yaml"
        with open(test_path, "w") as file:
            file.write(layer_content)
        assert test_path.is_file()

        schema = SOLARNETSchema(
            schema_layers=[test_path],
            use_defaults=True,
        )

        assert schema.attribute_schema is not None
        attribute_key = schema.attribute_schema["attribute_key"]
        # Assert Test Attribute is Added to the Schema
        assert "test_attribute" in schema.attribute_schema["attribute_key"]
        assert schema.attribute_schema["attribute_key"]["test_attribute"]["required"]
        # Assert AUTHOR is Overwritten in Schema
        assert "AUTHOR" in schema.attribute_schema["attribute_key"]
        assert not schema.attribute_schema["attribute_key"]["AUTHOR"]["required"]


def test_load_yaml_data():
    """Test Loading Yaml Data for Schema Files"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # This function writes invalid YAML content into a file
        invalid_yaml = """
        name: John Doe
        age 30
        """

        with open(tmpdirname + "test.yaml", "w") as file:
            file.write(invalid_yaml)

        # Load from an non-existant file
        with pytest.raises(yaml.YAMLError):
            _ = SOLARNETSchema()._load_yaml_data(tmpdirname + "test.yaml")
