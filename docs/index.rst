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

This specification is licensed under the Creative Commons Attribution 4.0 International Public License. For more information see the `LICENSE.txt`_ in our `GitHub Repository`_ or the `Creative Commons website`_.

.. _LICENSE.txt: https://github.com/IHDE-Alliance/solarnet_metadata/blob/main/LICENSE.txt
.. _GitHub Repository: https://github.com/IHDE-Alliance/solarnet_metadata
.. _Creative Commons website: https://creativecommons.org/licenses/by/4.0/

If you want to find the latest released or past version, see the releases. To provide comments or suggestions, please create an issue or a pull request, or contact prits-group@astro.uio.no.

.. raw:: html

   <div style="text-align: center;">
      <span class="new">Recent significant changes are highlighted in yellow.</span>
   </div>

Abstract
--------

Prior to these SOLARNET [#footnote1]_ recommendations, metadata descriptions of solar observations have been standardized only for space-based observations, but the standards have been mostly within a single mission at a time - at times with significant differences between different missions. Ground-based solar observations have typically not been made freely available to the general community, resulting in an even greater lack of standards for metadata descriptions. This situation makes it difficult to construct multi-instrument archives/virtual observatories, and makes it difficult to write generic data analysis tools. The metadata recommendations in this document aim to remedy this, to foster more collaboration and data sharing by acting as a common reference for generic analysis software and for ingestion into solar virtual observatories. As part of this, we also introduce a set of new, flexible mechanisms to represent metadata in FITS files (see the list of Appendices).

These recommendations are currently being followed by at least nine data pipelines [#footnote2]_ . *Please notify prits-group@astro.uio.no if you use these recommendations so your pipeline can be added to the list*. We also highly recommend that you ask to be put on our mailing list for occasional discussions and announcements of changes (prior to implementation in the document itself). This is important to ensure we do not implement changes that have already been "locked in".

.. [#footnote1] The SOLARNET project was funded by the European Union's Horizon 2020 and FP7 programmes under grant agreements No 312495 and 824135. Version 2.0 of this document was the final version produced under these grants, but it keeps evolving as further needs and issues arise. 

.. [#footnote2] Solar Orbiter SPICE, SST CHROMIS/CRISP (SSTRED), AISAS/Lomnicky Stit COMP-S/SCD, SAMNET, Gregor HiFI/GFPI, ROB USET, Alma pipeline for Solar data (SOAP), INAF IBIS-A (IBIS data Archive), PADRE/MeDDEA

Release History
----------------

.. toctree::
   :maxdepth: 2

   whatsnew/index


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

User's Guide
------------
.. toctree::
   :maxdepth: 2

   user-guide/index

Developer's Guide
-----------------
.. toctree::
   :maxdepth: 2

   dev-guide/index

API Guide
----------

.. toctree::
   :maxdepth: 2

   api

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