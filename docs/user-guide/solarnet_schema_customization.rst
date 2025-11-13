.. _solarnet_schema_customization:

*******************************
Customizing the SOLARNET Schema
*******************************

Overview
========

The :py:class:`~solarnet_metadata.schema.SOLARNETSchema` class provides an interface to configure how metadata attributes are formatted in solar data products.
The class represents a schema for metadata attribute requirements, validation, and formatting.

It is important to understand the configuration options of :py:class:`~solarnet_metadata.schema.SOLARNETSchema` objects in order to attain the desired behavior of metadata attributes.

The :py:class:`~solarnet_metadata.schema.SOLARNETSchema` class has two main properties:

* The class contains an :py:attr:`~solarnet_metadata.schema.SOLARNETSchema.attribute_schema` property which configures the metadata attributes.
* Second, the class contains a :py:attr:`~solarnet_metadata.schema.SOLARNETSchema.default_attributes` property which provides default values for attributes when none are specified.

This guide details the format of the schema, how it's used, and how you can extend or modify it to meet your specific needs.

The schema is loaded from YAML (dict-like) files which can be combined to layer multiple schema elements into a single unified schema.
This allows extensions and overrides to the default schema, and allows you to create new schema configurations for specific file types and specific metadata requirements.

Creating a SOLARNET Schema
==========================

Creating a :py:class:`~solarnet_metadata.schema.SOLARNETSchema` object optionally includes passing one or more paths to schema files to layer on top of one another, and optionally whether to use the default base layer schema file.

You can specify the schema layers as a list of file paths (:py:attr:`List[pathlib.Path | str]`), and whether to use the default schema layer by setting the :py:attr:`use_defaults` parameter to :py:attr:`True` or :py:attr:`False`.

Here is an example of instantiation of a :py:class:`~solarnet_metadata.schema.SOLARNETSchema` object:

.. code-block:: python

  schema_layers = ["my_schema_layer_1.yaml", "my_schema_layer_2.yaml"]
  my_schema = SOLARNETSchema(
    schema_layers=schema_layers,
    use_defaults=True
  )

This will create a new schema object using the default SOLARNET schema, and will overlay the :py:attr:`layer_2` file over the :py:attr:`layer_1` file.
If there are no conflicts within the schema files, then their attributes will be merged, to create a superset of the two files.
If there are conflicts in the combination of schema layers, this is resolved in a latest-priority ordering.
That is, if there are conflicts or duplicate keys in :py:attr:`layer_1` that also appear in :py:attr:`layer_2`, then the second layer will overwrite the values from the first layer in the resulting schema.

Attribute Schema Format
=======================

The SOLARNET attribute schema is used to define metadata requirements for solar data files. 
The schema is configured through YAML files, with the default configuration in :file:`solarnet_metadata/data/SOLARNET_attr_schema.yaml`

The YAML file has two main sections:

1. The :py:attr:`attribute_key` section: contains a dictionary of attribute information, keyed by the metadata attribute name.
2. The :py:attr:`conditional_requirements` section: defines attributes that are required based on specific conditions.

Here's an example of the schema file format:

.. code-block:: yaml

  attribute_key:
    attribute_name:
      data_type: <string> # one of ['int', 'float', 'str', 'date', 'bool']
      default: <Any> | null 
      description: >
        Include a meaningful description of the attribute and context needed to understand its values.
      human_readable: <string> # Provides a default value for the keyword comment
      required: <string> # one of ['all', 'primary', 'obs', 'optional']
      valid_values: optional[list]
      pattern: optional[string]  # For attributes with variable indices (e.g., NAXISn, CTYPEia)
      origin: <string> # one of ['N', 'S', 'P', 'O'] (for more information, see Section 19)
  conditional_requirements:
    - condition_type: <string>
      condition_key: <string>
      condition_value: optional[string]
      required_attributes: <list>

Each of the keys for the :py:attr:`attribute_key` section is defined in the table below:

.. list-table:: Attribute Schema Keys
  :widths: 10 50 10 10
  :header-rows: 1

  * - Schema Key
    - Description
    - Data Type
    - Is Required?
  * - `attribute_name`
    - the name of the metadata attribute as it should appear in your data products
    - `str`
    - `True`
  * - `data_type`
    - the expected data type of the attribute (`int`, `float`, `str`, `date`, `bool`)
    - `str`
    - `True`
  * - `default`
    - a default value for the attribute if needed/desired
    - varies or `null`
    - `True`
  * - `description`
    - a description for the metadata attribute and context needed to understand its values
    - `str`
    - `True`
  * - `human_readable`
    - a human-readable version of the attribute name.
    - `str`
    - `True`
  * - `required`
    - whether the attribute is required in your data products (`all`, `primary`, `obs`, `optional`)
    - various
    - `True`
  * - `valid_values`
    - values that the attribute should be checked against
    - `list` or `null`
    - `False`
  * - `pattern`
    - regular expression pattern for attributes with variable indices (e.g., NAXISn, CTYPEia)
    - `str`
    - `False`
  * - `origin`
    - indicates the origin of the keyword attribute. For more information, see :ref:`19.0`
    - `str`
    - `True`


The :py:attr:`conditional_requirements` section defines when certain attributes are required based on other attribute values:

This functionality allows you to specify that certain attributes are only required when specific conditions are met, such as the value of another attribute.
This section is still under development and is planned to be expanded in future releases.

.. list-table:: Conditional Requirements Schema
  :widths: 10 50 10 10
  :header-rows: 1

  * - Schema Key
    - Description
    - Data Type
    - Is Required?
  * - `condition_type`
    - the type of condition that must be met (e.g., 'attribute_value')
    - `str`
    - `True`
  * - `condition_key`
    - the attribute name that the condition requirement is based on
    - `str`
    - `True`
  * - `condition_value`
    - the value that the condition requirement is based on
    - `str` or `null`
    - `True`
  * - `required_attributes`
    - a list of attribute names that are required if the condition is met
    - `list[str]`
    - `True`

For example, the schema includes conditional requirements based on observatory type:

.. code-block:: yaml

  - condition_type: 'attribute_value'
    condition_key: 'OBS_TYPE'
    condition_value: 'ground-based'
    required_attributes:
      - OBSGEO-X
      - OBSGEO-Y
      - OBSGEO-Z

This specifies that when `OBS_TYPE==ground-based`, the `OBSGEO-X`, `OBSGEO-Y`, and `OBSGEO-Z` attributes are required.

Creating and Using Attribute Files
==================================

You can create your own schema files to extend or override the default schema. YAML syntax allows for complex data structures like anchors and aliases to create reusable components.

.. code-block:: yaml

  # Example of custom schema extension
  attribute_key:
    CUSTOM_ATTR:
      data_type: str
      default: custom value
      description: A custom attribute for my specific application
      human_readable: Custom Attribute
      required: optional
      valid_values: 
      - value1
      - value2
      - value3
  
  conditional_requirements:
    - condition_type: "equals"
      condition_key: "INST_TYP"
      condition_value: "Custom_Instrument"
      required_attributes: ["CUSTOM_ATTR"]

You can then load this custom schema along with the defaults:

.. code-block:: python

  custom_schema = Path("custom_schema.yaml")
  schema = SOLARNETSchema(
    schema_layers=[custom_schema],
    use_defaults=True
  )

`More information on YAML syntax. <https://www.yaml.info/learn/index.html>`_
