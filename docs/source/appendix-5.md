(appendix-v)=
# Appendix V. Other recommendations or suggestions

(appendix-va)=
## Appendix V-a. File naming suggestions

Although file-naming recommendations are of little consequence to an SVO, they can be a big help for users to get an overview of files stored locally, so we will give some (hopefully helpful) suggestions below.

The file name should be given in the keyword `FILENAME` (this is useful in case the actual file name is changed). `FILENAME` is mandatory for fully SOLARNET-compliant Obs-HDUs.

We recommend that file names only contain letters `A-Z` and `a-z`, digits `0-9`, periods, underscores, and plus/minus signs. Each component of the file name should be separated with an underscore – not a minus sign. In this regard, a range may be considered a single component with a minus sign between the min and max values (such as start/end date). File name components with numerical values should be a) preceded with one or more identifying letters, and b) given in a fixed-decimal format, e.g., (`00.0300`). Variable-length string values should be post-fixed with underscores to a fixed length.

Another common practice has been to start the file name with the “instrument name” – although typically defined in a consistent manner only on a _per mission_ or _per observatory_ basis – i.e., collisions may appear with other missions. Thus, we recommend prefixing the instrument name with a mission or observatory identifier (e.g., `iris` for IRIS or `sst` for SST).

After the instrument name, the data level is normally encoded as e.g., “l0” and “l1” for level 0 and 1. Note, however, that the definitions of data levels are normally entirely project/instrument-specific and does not by itself uniquely identify what kinds of processing have been applied.

Within each data set it is often very useful to have file names that can be sorted by time when subject to a lexical sort (such as with `“ls”`). This requires that the next item in the file name should be the date and time (e.g., `YYYYMMDD_HHMMSS[.ddd]` or `YYYYMMDDTHHMMSS[.ddd]`). The `“d”` part is fractional seconds, with enough digits to distinguish between any two consecutive observations.

If the data might be made available (simultaneously) with e.g., different processing emphasis (e.g., trade-offs between resolution and noise level), an alphanumeric identifier[^footnote-9] of the processing mode should be added in order to ensure uniqueness of the file name.

[^footnote-9]: E.g.,a short form of the contents of `PRMODEn`, see Section8.2.

What comes next is highly instrument-specific, but attributes that specify the type of content should definitely be encoded, e.g., which filter and wavelength has been used, which type of optical set-up has been used, etc. In particular, the wavelength is very useful for those who are not familiar with a data set.

Note that if file names (including file type suffixes) are longer than 68 characters, it will have to be split over two or more lines in a FITS header using the OGIP 1.0 long string convention. Likewise, if file name lengths exceed 67 characters, a comma-separated list of file names cannot be represented with one line per file. Thus, file names using 67 or fewer characters is preferable for human readability of FITS headers.

The names of files containing different observations _must_ be unique – i.e., all files must be able to coexist in a single directory. If the above recommendations do not result in a unique name, some additional information _must_ be added. We previously recommended that file names be kept identical even if newer versions were produced, but the recommendation is now the opposite. Instead, the keyword `FILEVERP` (file version pattern) should be specified to highlight a version identifier included in the file name. E.g., a file named `solo_SPICE_sit-V01-2395.fits` and the subsequent version `solo_SPICE_sit-V02-2395.fits` should both have `FILEVERP``='solo_SPICE_sit-V*-2395.fits'`, where the asterisk identifies where the file version occurs in the file name. Using an asterisk means that the file version should be interpreted lexically, whereas a percentage sign should be used when the version number is not a fixed number of decimals. E.g., with file names `file_V2.fits` and `file_V12.fits`, using `FILEVERP``='file_V%.fits'` would ensure that the second file recognized as having a higher version number (thus superseding the first file).

(appendix-vb)=
## Appendix V-b.	Storing data in a single file or in separate files

From an SVO point of view, _each Obs-HDU represents a single “observation unit”_ that may be registered separately. Thus, the choice of putting such observation units into separate files or not does not matter to an SVO in terms of searchability, but it does matter in terms of the file sizes of data that may be served. However, the meta-observation mechanism may be used to circumvent this issue (see [Appendix III](#appendix-iii)).

However, some “typical use” aspects should still be considered – including how most existing utilities [^footnote-10] interact with observations of a particular type:

[^footnote-10]: Some utilities may prefer different grouping of HDUs with respect to separate vs. single files, but that issue may be solved by a utility program that is able to join HDUs in separate files into a single file and vice versa.

As a general rule, Obs-HDUs that would typically be analysed/used together and are seldom used as stand-alone products should be stored in the same file, whereas Obs-HDUs that are often analysed/used as stand-alone products should be stored in separate files. Furthermore, Obs-HDUs with data of fundamentally different types (e.g., filter images vs. spectra vs. Fabry-Pérot data vs. spectropolarimetry) should _not_ be put in the same file.

Obviously, data processed by separate pipelines cannot be stored in a single file (unless they are combined at a later stage).

**Examples and arguments in favour of a single file:**

- Data from different Stokes parameters (for the same wavelength) are normally analysed together and should be put together in a single file. In fact, different Stokes parameter values are normally stored in a single extension, with different parameters located at different data cube indices along a Stokes dimension, see Section 5.4.1. A corresponding `CTYPEi``='STOKES'` coordinate is defined to indicate which data cube index contains data for a particular Stokes parameter. Note, however, that the Meta-HDU mechanism may be used to stitch together HDUs along the Stokes dimension so different Stokes parameters may be stored in different files.
- Data from a spectrometer raster [^footnote-11] are normally stored in a single file, even though the data may contain information from multiple detector readout windows. They have normally been acquired in a synchronous fashion, and they may be analysed together in order to have better estimates of continuum values when performing line fitting.
- Pointing adjustments _in order to track_ solar features by means of solar rotation compensation or feature tracking should not automatically cause the data to be stored in separate files. This is somewhat dependent upon the frequency and magnitude of the tracking movements relative to the field of view, and the magnitude of any time gaps relative to the cadence, but we leave it up to the discretion of pipeline designers to determine when it is appropriate to split image sequences in such cases: if the data are suitable for making a single movie, store them in a single file (and a single HDU).
- Having too many files can lead to inefficiency both on a file system basis and on the level of utilities.
- Not least, having too many files will also be an inconvenience to users who want to look at file lists manually.

[^footnote-11]: Rasters are observations (usually spectrometric) collected by stepping a slit across the observation area.

**Examples and arguments in favour of separate files:**

- Observations with different `POINT_ID` values (see Section 7) should not be stored in the same file.
- Images/movies in different filters are often used as stand-alone products, even if a parallel observation in another filter exists. Thus, observations from different filters should be put in separate files.
- In a similar fashion, Fabry-Pérot scans of _separate wavelength regions_ should go in separate files. The same applies to similar observations such as from spectropolarimetry.
- Some observation series with very low cadence should be stored with each image in a separate file. The definition of “very low cadence”, however, is somewhat dependent on the type of data, the resolution, and the variability time scale of resolved features. The “normal use” of the data also matters: If images are largely used as stationary context for other observations, they should definitely go into separate files. This is typically the case for synoptic observation series, which are also normally of indefinite length and therefore must be split up one way or another anyway.
- Observations with significantly different starting and/or end times should _not_ be stored in a single file. “Significantly different” in this context means on the order of a few times the cadence/exposure time or larger – since there may be technical reasons for differences smaller than this.

An additional aspect is that grouping data into a single file makes it impossible to download “only the interesting part” of a data set for a given analysis purpose. However, given the guidelines above, we think this is unlikely to be an issue. Also, a future SVO could provide file splitting “services”, such as selecting only specific HDUs from multi-HDU files.

When an Obs-HDU (partially) overlaps in time and space with one or more HDUs stored in other files, `CCURRENT` (concurrent) may be set to a comma-separated list of its own file name plus the names of all files containing concurrent Obs-HDUs [^footnote-12].

[^footnote-12]: This is of course on a “best effort” basis for the pipelines!

`CCURRENT` serves as a pointer to other concurrent (and probably relevant) observations, but it also serves a purpose in grouping search results (see Section 7).

(appendix-vc)=
## Appendix V-c.	Obs-HDU content guidelines

In addition to guidelines determining how data should be stored in single vs. multiple files, we here give guidelines for what should be considered as single vs. multiple observational units – i.e., _what should be stored in a single vs. multiple Obs-HDUs within each file_.

Such guidelines can only be given heuristically, due to the large diversity of possible data sets.

Each Obs-HDU will be registered as an individual observation unit, with attributes such as duration, minimum/maximum wavelength etc. Such attributes may be important search terms, and this must be taken into account when considering what should be collected into a single Obs-HDU or not.

As with the guidelines for keeping data in single or multiple files, some “typical use” aspects must also be considered – including how most existing utilities [^footnote-13] interact with observations of a particular type. In addition, any “user convenience” issues should be taken into account.

[^footnote-13]: Some utilities may prefer different practices, but a relatively simple program that is able to split or join HDUs in specific dimensions would solve the problem.

**Some examples and arguments in favour of a single HDU:**

- If a Fabry-Pérot scan is stored with each exposure (each wavelength) as a separate HDU, a search made for data covering a particular wavelength inside the scan’s min/max range will not match any of the HDUs if the desired wavelength falls between the band passes of the individual exposures.
- Different Stokes parameters are so intrinsically tied to each other that they should be stored together in a single HDU. There is also an existing convention for how to do this, see Section 8.5 in the FITS Standard.
- If an observation is repeated with a more or less fixed cadence (except for small cadence variations caused by e.g., technical issues/limitations), this will not be immediately apparent if each repetition is stored as a separate HDU.
- Observations are often visualised by displaying slices of a multi-dimensional data array, sometimes also scanning through one of the dimensions in order to visualise it as a movie (though not necessarily in the time dimension). Data that are likely to be visualised in such ways should be put into a single HDU. In other words, all dimensions through which slicing or scanning may be desirable should be included in a single HDU [^footnote-14].
- Pointing changes in e.g., slit-jaw movies due to slit movements should not cause the movie to be split into separate HDUs, even if there are relatively large pointing changes associated with the starting of new rasters in a series.
- Uneven spatial sampling, e.g., dense in the centre and sparse in the periphery, should not cause the data to be separated into multiple HDUs, though note that a table lookup form of WCS coordinates must be used.
- Variable exposure times due to _Automatic Exposure Control (AEC)_ should not cause the exposures to be stored in separate HDUs – as long as the settings for the AEC is constant.

[^footnote-14]: In particular, the time dimension should be included when observations are repeated and are suitable to be presented as a movie. Repeated rasters have traditionally not been collected into single HDUs, but that may be because of their low cadence -causing relatively few files to be created during a single observation run. This is changing, however, and we recommend that repeated rasters should be joined into single HDUs which include the time dimension, e.g., `(x,y,lambda,t)`.

**Examples and arguments in favour of separate HDUs:**

- Observation units stored in separate files according to the guidelines [Appendix V-b](#appendix-vb) are of course stored as separate HDUs.
- If the readout of a spectrometer has gaps (i.e., only small portions of the spectrum are extracted, in “wavelength/readout windows”), the different wavelength windows should in general _not_ be stored in a single HDU, since that would falsely indicate to an inexperienced user that the observation unit covers the entire spectrum between the minimum and maximum wavelengths. (It is of course _possible_ to store such readout windows in a single HDU, but then one would need to use a tabulated coordinate along the “gap dimension”).
- Some observation series are made with alternating long and short exposure times. These should _not_ be collected in a single Obs-HDU, because of the resulting difficulty in describing the exposure time [^footnote-15] as well as the complexity that would be required in utilities in order to handle/display such data correctly. Instead, the data should be separated into one HDU with long exposures and one HDU with short exposures.
- Data that are often displayed side by side, such as images in different filters should be split into separate HDUs.

[^footnote-15]: The variable-keyword mechanism _could_ be used for e.g., `XPOSURE` if such data are stored in a single HDU, e.g., `(x,y,t,2)`, with `XPOSURE` stored as `(1,1,1,2)`. But this is much less self-explanatory than having two separate HDUs, and it would require users/utilities to be aware of the mechanisms and how to use them. Since it is not absolutely necessary to do it this way, the variable-keyword mechanism should not be used.

For very closely connected, parallel observations, it is preferable to handle the grouping of data into Obs-HDUs in the same way for all of the observations, even if they are not of the same type (e.g., repeated rasters and corresponding slit-jaw movies).

Bearing all of the above in mind, observations that fit the following description should be collected into a single HDU:

An array of data that has (quasi-)uniform spacing in each physical dimension, e.g., x, y, lambda, and time, and also has (quasi-)constant attributes such as pointing, exposure times, gain, filter, and other relevant settings.
