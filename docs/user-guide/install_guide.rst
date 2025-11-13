.. _install_guide:

************************************
Installing SOLARNET Metadata Package
************************************

Installation Overview
=====================

.. note::
    **Beta Development Notice**: The SOLARNET Metadata Package is currently in beta development and may have frequent releases to PyPI.

The package can be installed via `pip <https://pip.pypa.io/en/stable/>`_ from the Python Package Index (PyPI). 
It is recommended to install the package within a virtual environment to avoid conflicts with other Python packages. 
You can find more information about the package at `https://pypi.org/project/solarnet_metadata/ <https://pypi.org/project/solarnet_metadata/>`_.

.. code-block:: bash

     pip install solarnet-metadata

Validate Installation
=====================

To validate that SOLARNET Metadata Package has been installed correctly, you can try importing the package in a Python environment:

.. code-block:: python

     from solarnet_metadata.validation import validate_file
     from pathlib import Path
     validate_file(Path("path/to/your/file.fits"))
