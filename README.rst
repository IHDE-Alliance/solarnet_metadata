SOLARNET Metadata Recommendations for Solar Observations
========================================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs| |readthedocs|
    * - build status
      - |testing| |codestyle| |coverage|
    * - Project Information
      - |DOI| |CODE_OF_CONDUCT|

.. |docs| image:: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/docs.yml/badge.svg
    :target: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/docs.yml
    :alt: Documentation Build Status

.. |testing| image:: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/testing.yml/badge.svg
    :target: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/testing.yml
    :alt: Build Status

.. |codestyle| image:: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/codestyle.yml/badge.svg
    :target: https://github.com/IHDE-Alliance/solarnet_metadata/actions/workflows/codestyle.yml
    :alt: Codestyle and linting using flake8

.. |coverage| image:: https://codecov.io/gh/IHDE-Alliance/solarnet_metadata/graph/badge.svg?token=PZLLKDTPGU
    :target: https://codecov.io/gh/IHDE-Alliance/solarnet_metadata
    :alt: Testing coverage

.. |readthedocs| image:: https://readthedocs.org/projects/solarnet-metadata/badge/?version=latest
    :target: https://solarnet-metadata.readthedocs.io/en/latest/?badge=latest
    :alt: ReadTheDocs Status

.. |DOI| image:: https://zenodo.org/badge/794299551.svg
    :target: https://doi.org/10.5281/zenodo.15741506
    :alt: DOI

.. |CODE_OF_CONDUCT| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
    :target: CODE_OF_CONDUCT.md
    :alt: Contributor Covenant Code of Conduct


.. end-badges

Stein Vidar Hagfors Haugan @steinhh, Terje Fredvik @tfredvik

Until the advent of the SOLARNET recommendations, metadata descriptions of Solar observations have been standardized for space-based observations, but the standards have been mostly within a single space mission at a time, at times with significant differences between different mission standards. In the context of ground-based Solar observations, data has typically not been made freely available to the general research community, resulting in an even greater lack of standards for metadata descriptions. This situation makes it difficult to construct multi-instrument archives/virtual observatories with anything more than the most basic metadata available for searching, as well as making it difficult to write generic software for instrument-agnostic data analysis. This document describes the metadata recommendations developed under the SOLARNET EU project, which aims foster more collaboration and data sharing between both ground-based and space-based Solar observatories. The recommendations will be followed by data pipelines developed under the SOLARNET project and others (Solar Orbiter SPICE, SST CHROMIS/CRISP (SSTRED), AISAS/Lomnicky Stit COMP-S/SCD, SAMNET, Gregor HiFI/GFPI, ROB USET, Alma pipeline for Solar data (SOAP), INAF IBIS-A (IBIS data Archive), PADRE/MeDDEA). These recommendations are meant to function as a common reference to which even existing diverse data sets may be related, for ingestion into solar virtual observatories and for analysis by generic software.

The original development of this work received funding from the European Union’s Horizon 2020 and FP7 programmes under grant agreements No 824135 and 31295. Version 2.0 of this document was the final version produced under these grants.

Documentation
-------------

The latest rendered documentation can be found on `readthedocs <http://solarnet-metadata.rtfd.io/>`_.

Acknowledging or Citing The SOLARNET Metadata Recommendations
-------------------------------------------------------------

If you use the SOLARNET Metadata Recommendations in your scientific work, we would appreciate your `citing it in your publications <http://solarnet-metadata.readthedocs.io/en/latest/citation.html>`_.
The continued growth and development of the SOLARNET Metadata Recommendations is dependent on the community being aware of them.

Building the Documentation Locally
----------------------------------

After cloning the repository, you can build the documentation locally by running the following commands:

.. code-block:: bash

    cd docs
    make clean
    make html  # Generates HTML in _build/html
    make latex && cd _build/latex && make && cd ../..  # Generates PDF in _build/latex
