.. _templates:

***************************
SOLARNET Metadata Templates
***************************

The SOLARNET Schema provides several useful methods for working with metadata attributes. 

- **Keyword Templates:** :py:class:`astropy.io.fits.Header` objects can be created as templates based on input options, where the header contains all default and required attributes with empty values. 
    - This enables users to easily fill in the necessary metadata for their data products in an partially populated FITS header format.
- **Keyword Detail Information:** You can also retrieve detailed information about specific attributes or all attributes in the schema. 
    - This is useful for understanding the requirements and context of each metadata attribute.
    - An :py:class:`astropy.table.Table` is returned, which can be easily viewed or exported to various formats (e.g., CSV, HTML).

Creating Attribute Templates
============================

Attributes templates are created using the :py:meth:`~solarnet_metadata.schema.SOLARNETSchema.attribute_template` method of the :py:class:`~solarnet_metadata.schema.SOLARNETSchema` class.
This method allows you to generate a template :py:class:`astropy.io.fits.Header` object populated with all required keywords, and values set to :py:attr:`None`.

This can serve as a useful tool for prototyping FITS header metadata that is compliant with the SOLARNET metadata standards.
Users can fill in the appropriate values for required attributes, and add optional attributes as needed to their headers. 

Options available for generating templates include:

- :py:attr:`primary` (bool): If :py:attr:`True`, the template will include keywords required for primary HDUs.
- :py:attr:`obs` (bool): If :py:attr:`True`, the template will include keywords required for observation HDUs.
- :py:attr:`observatory_type` (str): You can specify the type of observatory to include observatory-specific required keywords.
    - This must be one of ``["ground-based", "earth-orbiting", "deep-space"]``
- :py:attr:`instrument_type` (str): You can specify the type of instrument to include instrument-specific required keywords.
    - This must be one of ``["Imager", "Spectrograph"]``

.. code-block:: python

    from astropy.io import fits
    from solarnet_metadata.schema import SOLARNETSchema

    # Create a schema object
    schema = SOLARNETSchema(use_defaults=True)
    
    # Get a template for ground-based imager
    template: fits.Header = schema.attribute_template(
        primary=True,
        obs=True,
        observatory_type="ground-based",
        instrument_type="Imager"
    )

This returns a :py:class:`astropy.io.fits.Header` object where keys are required attribute names and values are :py:attr:`None`. You can then fill in the appropriate values for your data.


Getting Attribute Information
=============================

You can retrieve detailed information about specific attributes or all attributes using the `attribute_info()` method of the :py:class:`~solarnet_metadata.schema.SOLARNETSchema` class.

This method returns an :py:class:`astropy.table.Table` containing the attribute information.

Details provided include:

- Attribute name
- :py:attr:`data_type` (str): The expected data type of the attribute value.
- :py:attr:`default` (Any | None): The default value for the attribute, if any.
- :py:attr:`description` (str): A description of the attribute and its context.
- :py:attr:`human_readable` (str): Provides a default value for the keyword comment.
- :py:attr:`required` (str): Indicates if the attribute is required
- :py:attr:`origin` (str): Indicates the origin of the keyword attribute. For more information, see :ref:`19.0`
- :py:attr:`pattern` (str | None): For attributes with variable indices (e.g., NAXISn, CTYPEia), the pattern used to generate the attribute names.
- :py:attr:`valid_values` (list | None): A list of valid values for the attribute, if applicable.

You can optionally specify an attribute name with the :py:attr:`attribute_name` parameter to get information about a specific attribute.


For more information on the values provided, see the table in the :ref:`Attribute Schema Format <solarnet_schema_customization>` section.

.. code-block:: python

    from astropy.table import Table
    from solarnet_metadata.schema import SOLARNETSchema

    # Create a schema object
    schema = SOLARNETSchema(use_defaults=True)
    
    # Get information about a specific attribute
    author_info: Table = schema.attribute_info(attribute_name="AUTHOR")
    
    # Get information about all attributes
    all_info: Table = schema.attribute_info()

This returns an :py:class:`astropy.table.Table` containing all the schema information for the requested attribute(s).


Accessing Default Attributes
=============================

Default attributes can be specified in the schema for attributes that have a common default value.
These default values are loaded in the schema upon instantiation and are available through the :py:attr:`default_attributes` property of the :py:class:`~solarnet_metadata.schema.SOLARNETSchema` class.

The :py:attr:`default_attributes` property returns a :py:class:`astropy.fits.Header` object containing all attributes that have a specified default value in the schema, with their values set to the defined default.

The default attributes are included in the attribute templates generated by the :py:meth:`~solarnet_metadata.schema.SOLARNETSchema.attribute_template` method, with their values set to the specified default.

.. code-block:: python

    from astropy.io import fits
    from solarnet_metadata.schema import SOLARNETSchema

    # Create a schema object
    schema = SOLARNETSchema(use_defaults=True)
    
    # Get the default attributes
    defaults: fits.Header = schema.default_attributes

This can be useful for quickly populating a FITS header with common default values for required attributes in your data files.
The returned :py:class:`astropy.fits.Header` object can be easily manipulated or converted to other formats as needed.
