SOLARNET Metadata Recommendations for Solar Observations
========================================================

Stein Vidar Hagfors Haugan @steinhh, Terje Fredvik @tfredvik

Until the advent of the SOLARNET recommendations, metadata descriptions of Solar observations have been standardized for space-based observations, but the standards have been mostly within a single space mission at a time, at times with significant differences between different mission standards. In the context of ground-based Solar observations, data has typically not been made freely available to the general research community, resulting in an even greater lack of standards for metadata descriptions. This situation makes it difficult to construct multi-instrument archives/virtual observatories with anything more than the most basic metadata available for searching, as well as making it difficult to write generic software for instrument-agnostic data analysis. This document describes the metadata recommendations developed under the SOLARNET EU project, which aims foster more collaboration and data sharing between both ground-based and space-based Solar observatories. The recommendations will be followed by data pipelines developed under the SOLARNET project and others (Solar Orbiter SPICE, SST CHROMIS/CRISP (SSTRED), AISAS/Lomnicky Stit COMP-S/SCD, SAMNET, Gregor HiFI/GFPI, ROB USET, Alma pipeline for Solar data (SOAP), INAF IBIS-A (IBIS data Archive), PADRE/MeDDEA). These recommendations are meant to function as a common reference to which even existing diverse data sets may be related, for ingestion into solar virtual observatories and for analysis by generic software.

The original development of this work received funding from the European Union’s Horizon 2020 and FP7 programmes under grant agreements No 824135 and 31295. Version 2.0 of this document was the final version produced under these grants.

## Citing SOLARNET Metadata Recommendations

If you use the SOLARNET Metadata Recommendations in your work, we kindly ask that you cite the latest release in your publications.

- Latest Release: [![DOI](https://zenodo.org/badge/794299551.svg)](https://doi.org/10.5281/zenodo.15741506)
- Previous Versions:
    - Version 1.4 (March 2021) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5719255.svg)](https://doi.org/10.5281/zenodo.5719255)
    - Version 2.2 (March 2024) [![arXiv](https://img.shields.io/badge/arXiv-2011.12139v4-b31b1b.svg)](https://arxiv.org/abs/2011.12139v4)

The latest rendered documentation can be found on [readthedocs](http://solarnet-metadata.rtfd.io/).

## Building the Documentation Locally

After cloning the repository, you can build the documentation locally by running the following commands:

```bash
cd docs
make clean
make html  # Generates HTML in _build/html
make latex && cd _build/latex && make && cd ../..  # Generates PDF in _build/latex
```
