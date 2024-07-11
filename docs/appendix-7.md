## Appendix VII. External Extension References
In SOLARNET FITS files, in keywords that have no special function within the official FITS/WCS
framework, references to other extensions may be in the form of external extension references,
e.g.:

VAR_KEYS= '../auxiliary/s35837r001-aux.fits;VAR_KEY_DATA;TEMPERATURE[He_I]'

This means that the file with a relative path of '../auxiliary/' and a file name of 's35837r001-
aux.fits' contains a binary table with EXTNAME='VAR_KEY_DATA', containing a column with
TTYPEn='TEMPERATURE[He_I]' which holds the data for the variable keyword TEMPERATURE. The
path to the referenced file (s35837r001-aux.fits) is relative to the path of the referencing file.

In general terms, external extension references have the form '<relativepath>/<filename>;<extname>' and are drop-in replacements wherever plain extension names
may be used. The relative path must always start with either './' or '../'. In the example
above, the external extension reference is followed by a column name, just as if the external
extension reference was a regular extension name. When looking up the file to locate the
referenced extension, the software should allow for any file name variations due to compression
(e.g., endings like .gz and .zip).

***Placeholder extensions***
Of course, it may be that the end user does not have the file containing the external extension
available. To partially amend this situation, it is possible to have a placeholder extension in the
same file as the referring extension, containing the full header of the referenced extension but
having only a degenerate data cube (i.e., NAXISn=1). The EXTNAME of the placeholder extension
must be identical to the EXTNAME of the true external extension (i.e., 'VAR_KEY_DATA' in the
example above). The data dimensions of the true external extension should then be given in
XDIMNAn=NAXISn of the true external extension.