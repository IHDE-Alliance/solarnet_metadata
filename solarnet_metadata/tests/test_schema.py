import tempfile
from pathlib import Path

import astropy.io.fits as fits
import pytest
import yaml
from astropy.table import Table

from solarnet_metadata.schema import SOLARNETSchema
from solarnet_metadata.util import KeywordRequirement, load_yaml_data


def test_schema_default():
    """Test Creating a Schema with Default Parameters"""
    schema = SOLARNETSchema()

    # Attribute Schema
    assert schema.attribute_schema is not None
    assert isinstance(schema.attribute_schema, dict)

    # Attribute Key
    assert schema.attribute_key is not None
    assert isinstance(schema.attribute_key, dict)

    # Default Attributes
    assert schema.default_attributes is not None
    assert isinstance(schema.default_attributes, fits.Header)


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

        # Assert Test Attribute is Added to the Schema
        assert "test_attribute" in schema.attribute_key
        assert schema.attribute_key["test_attribute"]["required"]
        # Assert AUTHOR is Overwritten in Schema
        assert "AUTHOR" in schema.attribute_key
        assert not schema.attribute_key["AUTHOR"]["required"]


def test_load_yaml_data_non_existant_file():
    """Test Loading Yaml Data for Schema Files"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Load from an non-existant file
        with pytest.raises(FileNotFoundError):
            _ = load_yaml_data(tmpdirname + "non_existant_file.yaml")


def test_load_yaml_data_bad_data():
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
            _ = load_yaml_data(tmpdirname + "test.yaml")


def test_schema_load_default_attributes():
    """Test Getting the Default Attributes from the Schema"""
    schema = SOLARNETSchema()
    header = schema.default_attributes

    # Verify it's a FITS header
    assert isinstance(header, fits.Header)

    # Verify that attributes with defaults are included
    for keyword, info in schema.attribute_key.items():
        if info.get("default") is not None:
            assert keyword in header
        else:
            assert keyword not in header


@pytest.mark.parametrize(
    "data_type,default_value,expected_result,expected_data_type",
    [
        ("bool", "True", True, bool),
        ("int", "42", 42, int),
        ("float", "3.14", 3.14, float),
        ("str", "test", "test", str),
        (
            "date",
            "2021-01-01T00:00:00",
            "2021-01-01T00:00:00",
            str,
        ),  # FITS Header does not support datetime objects
        ("unknown", "value", "value", str),
        ("int", "not_an_int", "not_an_int", str),  # Tests exception handling
        ("str", "null", None, type(None)),  # Tests handling of 'null' string
    ],
)
def test_default_attributes_data_type_handling(
    data_type, default_value, expected_result, expected_data_type
):
    """Test handling of different data types when loading default attributes"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create schema with a single attribute with the specified data type and default
        schema_content = f"""
        attribute_key:
            TEST_ATTR:
                data_type: {data_type}
                default: {str(default_value)}
                human_readable: Test Attribute
                required: optional
        """

        test_path = Path(tmpdirname) / "test_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        # Create a schema with our test file
        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)
        header = schema.load_default_attributes()

        # Check the result
        if expected_result is not None:
            assert "TEST_ATTR" in header
            assert header["TEST_ATTR"] == expected_result
            assert header.comments["TEST_ATTR"] == "Test Attribute"
            assert isinstance(header["TEST_ATTR"], expected_data_type)
        else:
            assert "TEST_ATTR" not in header


def test_load_default_attributes_empty_schema():
    """Test loading default attributes with an empty schema"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create an empty schema file
        schema_content = """
        attribute_key: {}
        """

        test_path = Path(tmpdirname) / "test_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)
        header = schema.load_default_attributes()

        # Should return an empty header
        assert isinstance(header, fits.Header)
        assert len(header) == 0


def test_get_required_keywords_empty_schema():
    """Test get_required_keywords with an empty schema"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create empty schema file
        schema_content = """
        attribute_key: {}
        """
        test_path = Path(tmpdirname) / "empty_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)
        required_keywords = schema.get_required_keywords()

        # Should return an empty dictionary
        assert isinstance(required_keywords, dict)
        assert len(required_keywords) == 0


def test_get_required_keywords_with_default_schema():
    """Test with the default schema to ensure it handles real data properly"""
    schema = SOLARNETSchema(use_defaults=True)

    # Test with different parameter combinations
    all_keywords = schema.get_required_keywords(primary=False, obs=False)
    primary_keywords = schema.get_required_keywords(primary=True, obs=False)
    obs_keywords = schema.get_required_keywords(primary=False, obs=True)
    all_required = schema.get_required_keywords(primary=True, obs=True)

    # The primary-only set should include all ALL keywords plus PRIMARY-only keywords
    for key in all_keywords:
        assert key in primary_keywords

    # The obs-only set should include all ALL keywords plus OBS-only keywords
    for key in all_keywords:
        assert key in obs_keywords

    # The combined set should include everything from primary and obs sets
    assert set(all_required.keys()) == set(primary_keywords.keys()) | set(
        obs_keywords.keys()
    )

    # Verify that known required keywords from the default schema are present
    # This depends on the actual default schema, so we'll check a few known ones
    if "BITPIX" in schema.attribute_key:
        assert "BITPIX" in primary_keywords  # Primary HDU keyword

    if "BTYPE" in schema.attribute_key:
        assert "BTYPE" in obs_keywords  # Observation HDU keyword


@pytest.mark.parametrize(
    "primary, obs, expected_requirement_types",
    [
        (False, False, [KeywordRequirement.ALL]),
        (True, False, [KeywordRequirement.ALL, KeywordRequirement.PRIMARY]),
        (False, True, [KeywordRequirement.ALL, KeywordRequirement.OBS]),
        (
            True,
            True,
            [
                KeywordRequirement.ALL,
                KeywordRequirement.PRIMARY,
                KeywordRequirement.OBS,
            ],
        ),
    ],
)
def test_get_required_keywords_parameter_combinations(
    primary, obs, expected_requirement_types
):
    """Test different combinations of primary and obs parameters"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create test schema with all requirement types
        schema_content = """
        attribute_key:
            ALL_KEYWORD:
                description: Required for all HDUs
                default: null
                required: all
                data_type: str
                human_readable: Required for all
            PRIMARY_KEYWORD:
                description: Required for primary HDUs
                default: null
                required: primary
                data_type: str
                human_readable: Required for primary
            OBS_KEYWORD:
                description: Required for observation HDUs
                default: null
                required: obs
                data_type: str
                human_readable: Required for observation
            OPTIONAL_KEYWORD:
                description: Optional keyword
                default: null
                required: optional
                data_type: str
                human_readable: Optional
        """
        test_path = Path(tmpdirname) / "test_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)
        required_keywords = schema.get_required_keywords(primary=primary, obs=obs)

        # Verify correct keywords are returned
        assert isinstance(required_keywords, dict)

        # Ensure Optional keyword is not included
        assert "OPTIONAL_KEYWORD" not in required_keywords

        # Check that only the expected keywords are included
        expected_keywords = []
        if KeywordRequirement.ALL in expected_requirement_types:
            expected_keywords.append("ALL_KEYWORD")
        if KeywordRequirement.PRIMARY in expected_requirement_types:
            expected_keywords.append("PRIMARY_KEYWORD")
        if KeywordRequirement.OBS in expected_requirement_types:
            expected_keywords.append("OBS_KEYWORD")

        assert set(required_keywords.keys()) == set(expected_keywords)

        # Verify the returned keyword info is complete
        for keyword in required_keywords:
            assert "description" in required_keywords[keyword]
            assert "required" in required_keywords[keyword]
            assert "data_type" in required_keywords[keyword]


def test_attribute_template_default():
    """Test attribute_template with default parameters"""
    schema = SOLARNETSchema()
    template = schema.attribute_template()

    # Should return a FITS header with default attributes
    assert isinstance(template, fits.Header)
    # Default template should include all default attributes
    assert template == schema.default_attributes


def test_attribute_template_with_observatory_type():
    """Test attribute_template with observatory_type parameter"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create schema with conditional requirements for observatory_type
        schema_content = """
        attribute_key:
            OBS_TYPE:
                data_type: str
                default: null
                required: optional
                human_readable: Observatory Type
                valid_values: ["ground-based", "earth-orbiting", "deep-space"]
            OBSGEO-X:
                data_type: float
                default: null
                required: optional
                human_readable: Observatory X Coordinate
            OBSGEO-Y:
                data_type: float
                default: null
                required: optional
                human_readable: Observatory Y Coordinate
            OBSGEO-Z:
                data_type: float
                default: null
                required: optional
                human_readable: Observatory Z Coordinate
        conditional_requirements:
            - condition_type: attribute_value
              condition_key: OBS_TYPE
              condition_value: ground-based
              required_attributes:
                - OBSGEO-X
                - OBSGEO-Y
                - OBSGEO-Z
        """
        test_path = Path(tmpdirname) / "observatory_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)

        # Test with valid observatory_type
        template = schema.attribute_template(observatory_type="ground-based")

        # Verify conditional requirements are included
        assert "OBSGEO-X" in template
        assert "OBSGEO-Y" in template
        assert "OBSGEO-Z" in template

        # Test with invalid observatory_type
        template_invalid = schema.attribute_template(observatory_type="invalid-type")

        # Conditional requirements should not be included
        assert "OBSGEO-X" not in template_invalid
        assert "OBSGEO-Y" not in template_invalid
        assert "OBSGEO-Z" not in template_invalid


def test_attribute_template_with_instrument_type():
    """Test attribute_template with instrument_type parameter"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create schema with conditional requirements for instrument_type
        schema_content = """
        attribute_key:
            INST_TYP:
                data_type: str
                default: null
                required: optional
                human_readable: Instrument Type
                valid_values: ["Imager", "Spectrograph"]
            SPECSYS:
                data_type: str
                default: null
                required: optional
                human_readable: Spectral Reference Frame
            WAVELNTH:
                data_type: float
                default: null
                required: optional
                human_readable: Characteristic Wavelength
        conditional_requirements:
            - condition_type: attribute_value
              condition_key: INST_TYP
              condition_value: Spectrograph
              required_attributes:
                - SPECSYS
            - condition_type: attribute_value
              condition_key: INST_TYP
              condition_value: Imager
              required_attributes:
                - WAVELNTH
        """
        test_path = Path(tmpdirname) / "instrument_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)

        # Test with Spectrograph instrument_type
        template_spectro = schema.attribute_template(instrument_type="Spectrograph")

        # Verify Spectrograph conditional requirements are included
        assert "SPECSYS" in template_spectro
        assert "WAVELNTH" not in template_spectro

        # Test with Imager instrument_type
        template_imager = schema.attribute_template(instrument_type="Imager")

        # Verify Imager conditional requirements are included
        assert "WAVELNTH" in template_imager
        assert "SPECSYS" not in template_imager


def test_attribute_template_combined_parameters():
    """Test attribute_template with combined parameters"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create schema with both primary/obs requirements and conditional requirements
        schema_content = """
        attribute_key:
            PRIMARY_KEYWORD:
                data_type: str
                default: null
                required: primary
                human_readable: Required for primary
            OBS_KEYWORD:
                data_type: str
                default: null
                required: obs
                human_readable: Required for observation
            OBS_TYPE:
                data_type: str
                default: null
                required: optional
                human_readable: Observatory Type
                valid_values: ["ground-based", "earth-orbiting"]
            INST_TYP:
                data_type: str
                default: null
                required: optional
                human_readable: Instrument Type
                valid_values: ["Imager", "Spectrograph"]
            OBSGEO-X:
                data_type: float
                default: null
                required: optional
                human_readable: Observatory X Coordinate
            SPECSYS:
                data_type: str
                default: null
                required: optional
                human_readable: Spectral Reference Frame
        conditional_requirements:
            - condition_type: attribute_value
              condition_key: OBS_TYPE
              condition_value: ground-based
              required_attributes:
                - OBSGEO-X
            - condition_type: attribute_value
              condition_key: INST_TYP
              condition_value: Spectrograph
              required_attributes:
                - SPECSYS
        """
        test_path = Path(tmpdirname) / "combined_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)

        # Test with all parameters
        template = schema.attribute_template(
            primary=True,
            obs=True,
            observatory_type="ground-based",
            instrument_type="Spectrograph",
        )

        # Verify all requirements are included
        assert "PRIMARY_KEYWORD" in template
        assert "OBS_KEYWORD" in template
        assert "OBSGEO-X" in template
        assert "SPECSYS" in template


def test_attribute_info_all():
    """Test getting info for all attributes"""
    schema = SOLARNETSchema()
    info = schema.attribute_info()

    # Should return a Table
    assert isinstance(info, Table)

    # Should contain all attributes in the schema
    assert len(info) == len(schema.attribute_key)

    # Should have 'Attribute' column with all attribute names
    assert set(info["Attribute"]) == set(schema.attribute_key.keys())

    # Check that required columns exist
    assert "description" in info.columns
    assert "default" in info.columns
    assert "required" in info.columns


def test_attribute_info_specific():
    """Test getting info for a specific attribute"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create schema with test attributes
        schema_content = """
        attribute_key:
            TEST_ATTR:
                description: Test attribute description
                default: test_value
                required: optional
                data_type: str
                human_readable: Test Attribute
            ANOTHER_ATTR:
                description: Another attribute
                default: null
                required: all
                data_type: int
                human_readable: Another Attribute
        """
        test_path = Path(tmpdirname) / "test_schema.yaml"
        with open(test_path, "w") as file:
            file.write(schema_content)

        schema = SOLARNETSchema(schema_layers=[test_path], use_defaults=False)

        # Get info for specific attribute
        info = schema.attribute_info(attribute_name="TEST_ATTR")

        # Should return a DataFrame with one row
        assert isinstance(info, Table)
        assert len(info) == 1
        assert info["Attribute"][0] == "TEST_ATTR"
        assert info["description"][0] == "Test attribute description"
        assert info["default"][0] == "test_value"
        assert info["required"][0] == "optional"


def test_attribute_info_nonexistent():
    """Test error handling for nonexistent attribute"""
    schema = SOLARNETSchema()

    # Should raise KeyError for nonexistent attribute
    with pytest.raises(KeyError, match="Cannot find attribute name: NONEXISTENT"):
        schema.attribute_info(attribute_name="NONEXISTENT")
