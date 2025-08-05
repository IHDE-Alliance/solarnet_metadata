.. Solarnet documentation master file, created by
   sphinx-quickstart on Thu May  2 12:38:23 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SOLARNET Metadata Recommendations for Solar Observations
========================================================

.. raw:: html

   <div style="text-align: center;">
      Stein Vidar Hagfors Haugan, Terje Fredvik
   </div>

This specification is licensed under the Creative Commons Attribution 4.0 International Public License.
For more information see the `LICENSE.txt`_ in our `GitHub Repository`_ or the `Creative Commons website`_.

.. _LICENSE.txt: https://github.com/IHDE-Alliance/solarnet_metadata/blob/main/LICENSE.txt
.. _GitHub Repository: https://github.com/IHDE-Alliance/solarnet_metadata
.. _Creative Commons website: https://creativecommons.org/licenses/by/4.0/

If you want to find the latest released or past version, see the releases.
To provide comments or suggestions, please create an issue or create a pull request.

.. raw:: html

   <div style="text-align: center;">
      <span class="new">Recent significant changes are highlighted in yellow.</span>
   </div>

Abstract
--------

Prior to these recommendations, metadata descriptions of solar observations have been standardized only for space-based observations, but the standards have been mostly within a single space mission at a time - at times with significant differences between different missions. For ground-based solar observations, data has typically not been made freely available to the general community, resulting in an even greater lack of standards for metadata descriptions. This situation makes it difficult to construct multi-instrument archives/virtual observatories with anything more than the most basic metadata available for searching, as well as making it difficult to write generic tools for instrument-agnostic data analysis. This document describes metadata recommendations developed under the SOLARNET EU project [#footnote1]_ , aiming to foster more collaboration and data sharing between both ground-based and space-based solar observatories by acting as a common reference to which even existing diverse data sets may be related, for ingestion into solar virtual observatories and for analysis by generic software.

The recommendations are currently being followed by at least nine data pipelines [#footnote2]_ . *Please notify prits-group@astro.uio.no if you use these recommendations so you can be added to the list*. Since the document is still evolving, we also highly recommend that you ask to be put on our mailing list for discussions and announcements of changes (prior to implementation in the document itself). This is important to ensure we do not implement changes that have already been "locked in".

.. [#footnote1] This document has received funding from the European Union's Horizon 2020 and FP7 programmes under grant agreements No 824135 and 31295. Version 2.0 of this document was the final version produced under these grants, but it keeps evolving as further needs and issues arise. 


.. [#footnote2] Solar Orbiter SPICE, SST CHROMIS/CRISP (SSTRED), AISAS/Lomnicky Stit COMP-S/SCD, SAMNET, Gregor HiFI/GFPI, ROB USET, Alma pipeline for Solar data (SOAP), INAF IBIS-A (IBIS data Archive), PADRE/MeDDEA

Part A. Description of FITS Keywords
------------------------------------
.. toctree::
   :maxdepth: 3
   
   generated/parta.md
   appendix.rst

Part B. Lists of Mandatory and Optional FITS Keywords with Example Values
-------------------------------------------------------------------------
.. toctree::
   :maxdepth: 3

   generated/partb

Part C. Part C. Alphabetical listings of FITS keywords with section references
------------------------------------------------------------------------------
.. toctree::
   :maxdepth: 3

   generated/partc

Version Guidelines
------------------
.. toctree::
   :maxdepth: 0

   version_guidelines

Citation and Acknowledgements
-----------------------------
.. toctree::
   :maxdepth: 0

   citation

References
----------
.. toctree::
   :maxdepth: 3

   references

* :ref:`genindex`
* :ref:`search`