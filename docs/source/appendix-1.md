(appendix-i)=
# Appendix I. Variable-keyword mechanism

In many cases, auxiliary data such as detector temperatures, atmospheric conditions, variable exposure times, or adaptive optics performance is recorded alongside the observations. In some cases, other kinds of information such as the instrument response as a function of wavelength or a collection of instrument temperatures may be significant for correct interpretation of the data. In these cases, the variable-keyword mechanism described below can be used to link the observational data and the auxiliary data together. It can also be used to define array-valued keywords.

Since this mechanism may be used by any HDU with a non-zero `SOLARNET` keyword, we will from now on simply use the term “referring HDU” for an HDU that uses this mechanism. The actual values of a variable keyword are most commonly stored in a binary table column (called “value columns” in the description below), but image extensions may also be used (see [Appendix I-d](#appendix-id)). A specification of binary table extensions can be found in Cotton et al. 1995.

To use this mechanism, the referring HDU must contain the keyword `VAR_KEYS` declaring the `EXTNAME` of the binary table extension containing the value followed by a semicolon, and then a comma-separated list of the variable keywords.

When multiple extensions are used for storing variable keyword values, this is signalled by a comma behind the last keyword of one extension, then a new `EXTNAME` followed by a semicolon, then a comma-separated list of keywords stored in that extension. The `EXTNAME` is freely chosen as long as it adheres to the `EXTNAME` rules given in Section 2.

Each keyword name may be followed by a “tag” – a string surrounded by square brackets. The tag string itself may not contain semicolons, commas, or square brackets. The tag’s only function is to distinguish between different value columns containing values for the same keyword but applicable to different referring HDUs, if such a distinction is necessary. The tag can be chosen freely – but it may be useful for humans if it is derived from the `EXTNAME` of the referring HDU. However, multiple HDUs may refer to a single tagged value column if desired, in which case it may be useful to base the tag value on all referring HDUs’ extension names.

The value columns must have `TTYPEn` equal to the keyword name plus any tag. Column numbers (`n`) do not matter in the linking of value columns to keyword names. Note: _the CONTINUE Long String Keyword Convention must not be used with `TTYPEn`, since this is a reserved keyword defined in the FITS standard_. This means that the tag value may have to contain a shortened version of the referring HDUs’ extension names if such a scheme is used.

When appropriate, it is highly recommended that the referring HDU also contains a representative scalar value of a variable keyword, although this is not mandatory. How the representative value is chosen depends on the nature of the variable keyword, though the average of the variable values is usually the appropriate choice. Variable keywords may also have string values.

As an example, the header of a referring HDU might contain the following entries:

```none
EXTNAME = 'He_I ' / Referring HDU extension name
VAR_KEYS= 'VAR-EXT-1;KEYWD_1,KEYWD_2[He_I_He_II],VAR-EXT-2;KEYWD_3'/ Variable keywords
KEYWD_1 = 5.2 / Representative value (average) for KEYWD_1
KEYWD_2 = 4 / Representative value (maximum) for KEYWD_2
KEYWD_3 = 5 / Representative value (minimum) for KEYWD_3
```

This means that the values of the variable keywords `KEYWD_1` and `KEYWD_2` are stored in two separate columns in the `VAR-EXT-1` binary table extension, in columns named `'KEYWD_1'` and `'KEYWD_2[He_I_He_II]'`, respectively. Also, the `KEYWD_3` values are stored in the `VAR-EXT-2` binary table extension in a column named '`KEYWD_3`'. The “tag” `[He_I_He_II]` carries no intrinsic meaning, it is simply a text used to distinguish between columns in the `VAR-EXT-1` extension storing `KEYWD_2` values for different referring HDUs, e.g., `'[He_I_He_II]'` versus `'[O_V]'`. The `VAR-EXT-1` binary table header might contain the following entries (header examples from binary tables are shown in grey in this appendix):

```none
EXTNAME = 'VAR-EXT-1' / Variable keyword binary table extension name
:
TTYPE5 = 'KEYWD_1' / Column 5: values for KEYWD_1
TTYPE6 = 'KEYWD_2[He_I_He_II]' / Column 6: values for KEYWD_2 for He_I & He_II
TTYPE7 = 'KEYWD_2[C_II]' / Column 8: values for KEYWD_2 for C_II
```

The `TTYPE7` entry is included only to illustrate the need for the `[He_I_He_II]` tag in `TTYPE6`.

The `VAR-EXT-2` binary table extension might contain the following entries:

```none
EXTNAME = 'VAR-EXT-2' / Variable keyword binary table extension name
TTYPE1 = 'KEYWD_3' / Column 1 contains variable KEYWD_3 values
```

There are two ways in which the values of the variable keyword data cube may be associated with the data cube in the referring HDU: association by coordinates ([Appendix I-a](#appendix-ia)) and pixel-to-pixel association ([Appendix I-b](#appendix-ib)).

The mechanism described here may also be used to store a set of values that do _not_ vary as a function of any coordinate or dimension of the referring HDU. Such constant, multi-valued keywords are described in [Appendix I-d](#appendix-id).

In all the examples below, the referring HDU is an image sequence with coordinates and dimensions `[x,y,t]=[HPLN-TAN, HPLT-TAN, UTC]=[512,512,60]`, with a header containing the following entries relevant to the examples in this appendix (note the formatting of `VAR_KEYS` for readability – spaces are ignored in the interpretation of the keyword):

```none
DATEREF = '2023-02-01T00:00:00' / Time coord. zero point (time reference, mandatory)
CTYPE1 = 'HPLN-TAN' / Coord. 1 is ”solar x”
CTYPE2 = 'HPLT-TAN' / Coord. 2 is ”solar y”
CTYPE3 = 'UTC ' / Coord. 3 is time in seconds relative to DATEREF
NAXIS1 = 512 / Size of dimension 1
NAXIS2 = 512 / Size of dimension 2
NAXIS3 = 60 / Size of dimension 3
:
VAR_KEYS= 'MEASUREMENTS; &' / Extension containing measured auxiliary values
CONTINUE ' ATMOS_R0, &' / ATMOS_R0 values
CONTINUE ' TEMPS, &' / Temperatures
```

(appendix-ia)=
## Appendix I-a. Variable keywords using coordinate association

The variable-keyword mechanism using association by coordinates is fully analogous to the matching up of two separate observations – it is their shared coordinates that describe how to align the two in space, time, wavelength etc. In general, two Obs-HDUs do not necessarily have all coordinates in common. Examples are images vs. spectral rasters, or polarimetric data vs. images. Of course, the order of the WCS coordinates in the two Obs-HDUs does not matter, and e.g., the spatial, temporal, and spectral sampling of the observations may be entirely different, and the coordinates may even be irregular.

As with two separate Obs-HDUs, when using association by coordinates for variable keywords each value column has its own set of WCS keywords defining their WCS coordinates. These coordinates specify where each value in the value column data cube is located in relation to the referring HDU’s WCS coordinates.

As is the case for the alignment of e.g., images vs. spectra, the value columns do not need to specify all of the coordinates in the referring HDU (e.g., a time series of temperatures vs. a sequence of images) and may have coordinates that are not present in the referring HDU (e.g., a time series of temperatures vs. a single image in the referring HDU). Furthermore, it is the coordinate _name_ that is used to establish the association, after any projection has been taken into account. E.g., `HPLN-TAN` and `HPLN-TAB` are both recognised as just `HPLN` with respect to association.

If the value column contains no other coordinates than those present in the referring HDU, and no dimensions without a coordinate, only a single keyword value is associated with any pixel in the referring HDU. This is because the association uniquely determines the position within the value column based on the position in the referring HDU.

However, if the value column contains coordinates that are not present in the referring HDU, or dimensions without an assigned coordinate, there are multiple values within the value column that apply to any given pixel in the referring HDU.

**_Example 1 - Variable keywords associated by shared coordinate_**

Let us assume that the atmospheric coherence length `ATMOS_R0` is recorded independently during the observations described by the example header above, with a different temporal resolution than the observations.

For each exposure in the observation series, there is a single value of `ATMOS_R0` that applies to all pixels in that exposure. Thus, the `ATMOS_R0` value column should be one-dimensional, and the only coordinate that needs to be specified is time.

The header of the corresponding binary table extension `MEASUREMENTS` might contain the following entries:

```none
EXTNAME = 'MEASUREMENTS' / Extension containing measured auxiliary values
DATEREF = '2018-01-01T12:00:00' / Time coord. zero point (time reference, mandatory)
TTYPE5 = 'ATMOS_R0' / Column 5 contains values for ATMOS_R0
1CTYP5 = 'UTC ' / Time coordinate
TDIM5 = '(4700) ' / Array dimensions for column 5
```

As we can see, the value of `1CTYP5` is identical to the value of `CTYPE3` in the referring HDU described above. This is the only basis for determining association of coordinates. The coordinate numbers (`i=1` vs `i=3`) are irrelevant in the association, it is only the values of the UTC coordinate together with its zero-point `DATEREF` that matters in the matching up of the two data cubes. E.g., dimension numbers and sizes (`NAXIS3` vs `TDIM5`) are irrelevant. Note that `DATEREF` may very well be different between the two extensions, the times that are compared are the “sum” of `DATEREF` and the UTC coordinate calculated according to the standard coordinate formulas!

Now, in order to find the value of `ATMOS_R0` for a given point in the referring data cube, the time corresponding to that point must be calculated. A reverse calculation is done for the value column to locate the point where its time coordinate has the same value. Then, the `ATMOS_R0` value can be extracted from that point in the value column (using linear interpolation as specified in the FITS standard).

Note that the zero point for the time coordinate (`DATEREF`) _must_ be given for both extensions when one of the specified coordinates are `UTC`, and it applies to all columns with a `UTC` coordinate. Thus, if two value columns have different starting points, the relevant `iCRVLn` and/or `jCRPXn` values must be adjusted accordingly. This issue does not arise if the keyword values are stored as separate image extensions, see [Appendix I-d](#appendix-id).

If multiple values must be associated with each image, the value column would have one or more additional dimensions. The values for a given image would then be all values in the value column with a time coordinate matching that of the image. Such a scenario might arise if e.g., multiple temperatures inside the instrument is being recorded.

**_Example 2 – Variable keywords associated by multiple shared coordinates_**

Of course, the referring HDU and the value column may have more than one shared coordinate. In this case, the process is entirely analogous to the situation where there is only one shared coordinate: shared coordinate 1 and shared coordinate 2 are calculated for a pixel in the referring HDU, and these coordinates are then used to look up the correct value(s) in the value column, using its definition of the same coordinates.

**_Example 3 – Real-life example with multi-valued keyword associated by a single shared coordinate – with table look-up of coordinates!_**

As a complex, real-life example of how this mechanism can be used, we refer to CHROMIS FITS files, which contain values of R0 that are a function of time, but also a function of (two) different subfield sizes. Thus, there are two coordinates defined for the value column: time (UTC) and subfield size (WFSSZ, not a WCS coordinate). Both coordinates must be tabulated because they vary unevenly and cannot be described as linear functions of pixel coordinates. CHROMIS FITS files can be found in the SST archive at <https://dubshen.astro.su.se/sst_archive/>.

(appendix-ib)=
## Appendix I-b. Variable keywords using pixel-to-pixel association

Some variable keywords encode discrete-valued properties or properties that are sampled in exact sync with the observational data. In such cases, it might be important to ensure an exact correspondence between pixels in the referring HDU’s data cube and pixels in the value column’s data cube, without any round-off errors in the floating-point calculations of WCS coordinates.

When standard WCS calculations are used in the association between the referring HDU and the value column, such round-off errors may interfere with any exact pixel-to-pixel correspondence, resulting in a linear interpolation of the values in the value column. I.e., if a variable keyword represents a discrete-valued property, association by coordinates may result in non-discrete values. If instead a direct pixel-to-pixel association is desirable, the variable-keyword mechanism may be used as described below.

Even for non-discrete-valued keywords it may be simpler and more illustrative to use a pixel-to-pixel association. This is typically the case for values that have been measured in sync with the observations. Another example could be values varying along one detector dimension, e.g., one value per detector row.

In order to signal such an exact pixel-to-pixel association, the `WCSNn` keyword for the value column must start with `'PIXEL-TO-PIXEL'`. In this case, _no coordinate specified for the value column will be used in the association_. Also, all dimensions of the data cube in the referring HDU must be present in the value column (in the same order). Dimensions in the referring HDU for which the variable keyword has a constant value should be collapsed into singular dimensions in the value column. Trailing dimensions may be added in order to specify variable keywords with multiple values for each pixel in the referring HDU.

**_Example 4 – Variable keyword with pixel-to-pixel association_**

If the `ATMOS_R0` values from Example 1 in [Appendix I-a](#appendix-ia) had been recorded in sync with the 60 images, i.e., a single `ATMOS_R0` value is recorded for each image, the binary table extension might instead contain the following entries:

```none
EXTNAME = 'MEASUREMENTS' / Extension name of binary table extension
WCSN5 = 'PIXEL-TO-PIXEL' / Column 5 uses pixel-to-pixel association
TTYPE5 = 'ATMOS_R0' / Column 5 contains values for ATMOS_R0
TDIM5 = '(1,1,60)' / Array dimensions for column 5
```

This means that the `ATMOS_R0` value for any referring HDU pixel `(x,y,t)` is found in pixel `(1,1,t)` of the `ATMOS_R0` value column data cube.

The pixel-to-pixel association may also be used if `ATMOS_R0` had been recorded with a lower cadence than the images. If e.g., `ATMOS_R0` was recorded for every 20<sup>th</sup> image then the value found in in pixel `(1,1,1)` of the `ATMOS_R0` column data cube applies to the first 20 images, the value in pixel (1,1,2) applies to the next 20 images, etc. A total of 3 `ATMOS_R0` measurements would have been made during acquisition of the 60 images, thus `TDIM5='(1,1,3)'`.

Generically, when `WCSNn``='PIXEL-TO-PIXEL'`, if the size of a dimension _`j`_ in the variable keyword data cube is _`1/N`_ of the corresponding dimension of the data cube of the referring HDU, the pixel index _p<sub>j,v</sub>_ for the variable keyword data cube can be found from the referring HDU's data cube pixel index _p<sub>j,d</sub>_ through the formula _p<sub>j,v</sub>_ = _floor((p<sub>j,d</sub> - 1)/N)+1_.

If multiple values must be associated with each image, the value column would have one or more additional trailing dimensions. E.g., if two independent `ATMOS_R0` values were measured for each image, the value column would have `TDIM5='(1,1,60,2)'`. Thus, for pixel `(1,1,2)` in the referring HDU, the values `(1,1,2,*)` would apply.

(appendix-ic)=
## Appendix I-c. Array-valued keywords (no association)

It is possible to use the variable-keyword mechanism to specify keywords that are multi-valued but entirely independent of the referring HDU’s WCS coordinates i.e., simply an array-valued keyword. This is achieved simply by having no shared coordinates among the referring HDU and the value column. The value column may have any number of dimensions. A one-dimensional array-valued keyword is used in SPICE FITS files to record a list of lost telemetry packets for each readout window.

(appendix-id)=
## Appendix I-d. Using image extensions instead of binary tables

The variable-keyword mechanism may also be used with image extensions instead of binary table extensions. In this case, the `VAR_KEYS` keyword contains only extension names separated with a comma and a semicolon, ending with a semicolon. The name of the variable keyword is defined by the extension name, though the extension name may also contain a tag. I.e., `VAR_KEYS``='KEYWD_1 ;, KEYWD_2[He_I_He_II]; '` declares that values for `KEYWD_1` are to be found in image extension `KEYWD_1`, and values for `KEYWD_2` are to be found in image extension `KEYWD_2[He_I_He_II]`. In all other respects, this variant of the mechanism is analogous to the specification above using binary tables, with e.g., `WCSNAMEa` starting with `'PIXEL-TO-PIXEL'` to signal that pixel-to-pixel association is used.
