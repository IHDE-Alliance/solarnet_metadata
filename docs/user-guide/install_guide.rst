.. _install_guide:

************************************
Installing SOLARNET Metadata Package
************************************

Installation Overview
=====================

.. note::
    **Beta Development Notice**: The SOLARNET Metadata Package is currently in beta development and not yet available on PyPI. 
    The PyPI release capability will be added when the package is determined mature enough for its first official release.

Until the package is released on PyPI, it should be installed from GitHub using:

.. code-block:: bash

     pip install git+https://github.com/IHDE-Alliance/solarnet_metadata.git@solarnet_metadata_package

When the package is ready for PyPI, the branch will be merged into main and the package will be released to PyPI at 
`https://pypi.org/project/solarnet_metadata/ <https://pypi.org/project/solarnet_metadata/>`_, after which it can be installed using:

.. code-block:: bash

     pip install solarnet_metadata

Validate Installation
=====================

To validate that SOLARNET Metadata Package has been installed correctly, you can try importing the package in a Python environment:

.. code-block:: python

     from solarnet_metadata.validation import validate_file
     from pathlib import Path
     validate_file(Path("path/to/your/file.fits"))
