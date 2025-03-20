import pytest
import tempfile
from pathlib import Path
import yaml
import pandas as pd

from solarnet_metadata.schema import SOLARNETSchema

# Mock schema for testing
MOCK_SCHEMA = {
    "attribute_key": {
        "NAXIS": {"required": True, "data_type": "int"},
        "COMMENT": {"required": False},
        "AUTHOR": {"required": True, "data_type": "str"},
    },
    "conditional_requirements": [],
}


# Helper function to create a SOLARNETSchema instance with mock schema
def create_mock_schema():
    schema = SOLARNETSchema()
    schema._attr_schema = MOCK_SCHEMA
    return schema


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


# Parameterized test cases for the validate method
@pytest.mark.parametrize(
    "header, warn_no_comment, warn_data_type, expected_findings",
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
def test_validate(header, warn_no_comment, warn_data_type, expected_findings):
    schema = create_mock_schema()
    findings = schema.validate(header, warn_no_comment, warn_data_type)
    assert findings == expected_findings
