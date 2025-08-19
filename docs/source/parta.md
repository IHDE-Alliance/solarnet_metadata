(1.0)=
# 1. About file formats
<style>
  .new {
      background-color:rgb(252, 252, 147)
  }
</style>

The most common practice in the solar remote sensing community is currently to use the FITS Standard file format for disseminating solar remote sensing observations. For this reason, this document describes how to include the metadata content through keywords inside FITS files, but _that does not preclude the use of other file formats_. In many ways, this document simply uses FITS notation as a language to express the underlying metadata requirements.

For a discussion about file names and how to group observational data between or inside different files, see [Appendix V: Other recommendations](#appendix-v).

(2.0)=
# 2. Header and Data Units (HDUs) in FITS files

FITS files may contain one or more Header and Data Units (HDUs) of different types, e.g., primary HDUs, image extensions, and binary table extensions, containing data and a header with metadata stored as keyword-value pairs. Primary HDUs and image extensions are for almost all practical purposes identical: The primary HDU should simply be regarded as “_the first HDU, which must exist and is always an image HDU but is not required to contain any data, just a header”_. Thus, all SOLARNET recommendations applying to an extension HDU also applies to the primary HDU.

This document primarily describes how the SOLARNET recommendations apply when using primary and image HDUs to store observational data, but [Appendix IV](#appendix-iv) also explains how the recommendations may be applied to observational data stored in binary table extensions. In this context, observational data are data values derived from solar photons recorded by a detector. Other types of data, e.g., temperatures, voltages, atmospheric conditions etc., will be regarded as auxiliary data.

In this document, HDUs storing observational data will be referred to as Obs-HDUs.

There are many keywords that are not mentioned in this document which have an established definition in the FITS Standard, Papers I-V, Thompson (2006), other references, and existing or past projects. As far as possible, such keywords should be used when appropriate, and should not be used in conflict with that definition. New keywords should not be invented if there is already a keyword in established use that covers the needs of the keyword. In general, see the “Other sources of keywords with established use” from the References section before inventing a new keyword.

By default, FITS string values are limited to 68 characters, but the [CONTINUE Long String Convention](https://fits.gsfc.nasa.gov/registry/continue_keyword.html) (see [References](#reference_list)) may be used in order to allow keywords to contain strings longer than 68 characters. _Note that this convention must not be used with any of the mandatory or reserved keywords defined in the FITS standard_.

In order to prevent having to specify keyword information that is common to all HDUs in a file, keyword inheritance may be used according to the [FITS Header Inheritance Convention](https://fits.gsfc.nasa.gov/registry/inherit/fits_inheritance.txt) (see [References](#reference_list)).

This document introduces three new mechanisms that are not part of the FITS standards, but may be useful in fully describing observations: [Appendix I](#appendix-i) explains how to describe keywords that vary as a function of WCS coordinates, [Appendix I-d](#appendix-id) explains how to pin-point and (optionally) associate values to specific pixels/locations inside a data cube, and [Appendix III](#appendix-iii) explains how to signal that an HDU is a part of a larger set of HDUs (e.g., a time series) contained in multiple files.

(2.1)=
## 2.1 Naming of HDUs in SOLARNET FITS files

All HDUs – including the primary HDU – in SOLARNET FITS files _must_ contain the string-valued keyword `EXTNAME`, and each `EXTNAME` value must be unique within the file[^footnote-2]. `EXTNAME` must not contain the characters comma or semicolon except as prescribed for the variable-keyword mechanism ([Appendix I](#appendix-i)), the pixel list mechanism ([Appendix I-d](#appendix-id)) and the meta-observation mechanism ([Appendix III](#appendix-iii)). In addition, `EXTNAME` must not start with a space, but any trailing spaces are ignored. Finally, the CONTINUE Long String Keyword Convention must not be used with `EXTNAME`, since this is a reserved keyword defined in the FITS standard.

[^footnote-2]: There is one exception to the SOLARNET rule requiring unique `EXTNAME`s: As per the official FITS WCS mechanism for `Lookup` coordinate distortions, all extensions containing lookup tables must have `EXTNAME``=WCSDVARR`. These extensions must instead be distinguished by having different values of the seldom used FITS Standard `EXTVER` keyword.

(2.2)=
## 2.2 Fully and partially SOLARNET-compliant Obs-HDUs

All fully SOLARNET-compliant _and_ partially SOLARNET-compliant Obs-HDUs _must_ contain (in addition to all mandatory FITS standard keywords) the following mandatory keywords (this also applies to the primary HDU if it is an Obs-HDU):

```none
EXTNAME
SOLARNET
OBS_HDU
DATE-BEG
```

Obs-HDUs cannot contain keywords with definitions in conflict with other SOLARNET-defined keywords unless they occur in a comma-separated list in the keyword `SOLNETEX`. This mechanism may sometimes be necessary to ensure backwards compatibility with existing utilities. Keywords listed in `SOLNETEX` will be ignored by SOLARNET-aware utilities. The `SOLNETEX` mechanism must _not_ be applied to FITS standard keywords.

The `SOLARNET` keyword is used to signal if an Obs-HDU is fully SOLARNET-compliant (`SOLARNET``=1`) or partially SOLARNET-compliant (`SOLARNET``=0.5`).


Fully SOLARNET-compliant Obs-HDUs _must_ contain all mandatory SOLARNET/FITS standard keywords described in Section 15 that apply (depending on the nature of the observation) and _must not_ have any of those mandatory keywords listed in `SOLNETEX`.

Partially SOLARNET-compliant Obs-HDUs need not contain all keywords summarised in Section 15.

Both fully and partially SOLARNET-compliant Obs_HDUs _must_ have `OBS_HDU``=1`.

(2.3)=
## 2.3 Other HDUs

Other HDUs in the same file as an Obs-HDU may be used to store additional data that is required to describe the observations, to allow instrument-specific utilities to function correctly, to interpret the data correctly, or to enable further calibrations to be made. Specific cases of such HDUs are variable-keyword HDUs ([Appendix I](#appendix-i)), pixel list HDUs ([Appendix I-d](#appendix-id)) and Meta-HDUs ([Appendix III](#appendix-iii)).

Obs-HDUs that are neither fully nor partially SOLARNET-compliant may use the mechanisms described in 0, [Appendix I-d](#appendix-id) or [Appendix III](#appendix-iii), if they have `SOLARNET``=-1`. In fact, the HDUs described in these appendices may themselves use these mechanisms, if they have `SOLARNET``=-1`.

(2.4)=
## 2.4 Comments

We strongly urge pipeline designers to use the FITS mechanism for commenting keywords (using a forward slash after the keyword value). Although pipeline designers may know all their cryptic keywords by heart while writing the pipeline, this will not be the case a year or more later.

Any units for keyword values should be enclosed in square brackets at the beginning of the keyword comment (Section 4.3 of the FITS Standard).

We are considering making a machine- and human-readable catalogue of keyword comments used in this document, making it possible to create utilities that fill them out automatically for SOLARNET-defined keywords. However, the main utility of such a wrapper would be to also identify keywords with no comment at all, or comments without unit specifications (where appropriate).

Additional comments may be added using the `COMMENT` keyword or by leaving the keyword field blank – see Section 4.4.2.4 in the FITS Standard.

(3.0)=
# 3 The World Coordinate System (WCS) and related keywords

The World Coordinate System (WCS) is a very comprehensive standard that should be used for the description of physical data coordinates in Obs-HDUs.

In some earlier data sets, the data coordinates are not specified using the WCS standard, but rather through e.g., `XCEN`, `YCEN`, `FOVX`, and `FOVY`, etc. Future pipelines, however, should _only_ use the full, recommended WCS standard, without any deprecated features (e.g., `CROTAia`) or any instrument- or mission-specific practices[^footnote-3].

All keywords described in this Section are defined by the FITS Standard and Papers I-V. See also Thompson (2006).

[^footnote-3]: If a full description seems impossible through the existing WCS framework, create an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues).

(3.1)=
## 3.1 Fundamental WCS coordinate specification

As a reference, the most commonly used conversion from the set of pixel indices _(p<sub>1</sub>, p<sub>2</sub> p<sub>3,</sub> … p<sub>N</sub>)_ to a physical WCS coordinate is given by the following formula:

```{math}
c_i(p_1,p_2,p_3,...,p_N)=CRVAL{i} + CDELT{i}\sum_{j=1}^{N}PC{i\_j}(p_j-CRPIXj)
```

Thus, to calculate the physical (world) coordinates at any point within the data cube, the following entities are involved:

- `CRPIXja` values specify the data cube pixel indices for a “reference point”.
- `CRVALia` is the value of world coordinate i at this reference point.
- `PCi_ja` is a linear transformation matrix between data cube dimension j and coordinate axis i, which can be used to specify rotations, shear, transpositions and reflections.
- `CDELTia` is the increment of world coordinate i at the reference point.

Here, `j` goes from `1` to the number of data dimensions, i.e., from `1` to `NAXIS`, and `i` goes from `1` to the number of physical coordinates. The number of physical coordinates is normally equal to `NAXIS` but may be larger or smaller as optionally specified in `WCSAXES`. Cases in which `WCSAXES` are used to indicate a different number of dimensions than `NAXIS` could be e.g.:

- when trailing singular dimensions are being suppressed in the writing of the file, as happens in IDL.
- when there are more coordinates that vary throughout the data cube than there are data cube dimensions, e.g., in a raster scan with (x,y,lambda) coordinates, with a time coordinate that is also a function of the x coordinate.
- when dummy coordinates are used in table lookup of coordinates, in order to minimise the storage space requirements.

`CTYPEia` is used to specify the nature of the coordinates and their projections. In solar observations, the most appropriate values include `HPLN-TAN` and `HPLT-TAN` (solar coordinates; Thompson 2006), `WAVE` (wavelengths in vacuum; Paper III), `UTC` (time; Paper IV), and `STOKES` (Stokes parameter; Paper I).

Coordinates may also be given in table lookup form (Section 6 in Paper III), for use with e.g., Fabry-Pérot imaging spectroscopy with uneven spacing in the wavelength direction. Also, WCS even allows for specifications of distortions down to a pixel-by-pixel level basis if required (see Paper V).

In ground-based observations, image restoration techniques such as MOMFBD leave behind apparent local movements of image features. Such residual effects represent local errors/distortions in the coordinate system specified by the HDU’s WCS keywords. In the FITS Standard Section 8.2, it is specified that a “representative average” of such random errors may be given in the keywords `CRDERia` (for axis number `i`).

Likewise, representative averages for systematic errors in the coordinates may be given in the keywords `CSYERia` (for coordinate number `i`). Thus, `CSYERia` should be used to represent the uncertainty in the pointing/position of the image as a whole, and uncertainties in the wavelength calibration for spectrometric data.

If a coordinate system has been determined or refined through the use of some external reference image(s) or other source(s), or even been adjusted manually, the keyword `PRREFn` should be used to give a comma-separated list of the images/sources/people, see Section 8. If it is not possible to give specific image names/references, the name of the instrument, filter, etc. should be given. Since such images must obviously be (near) co-temporal with the data in the Obs-HDU, this should not introduce much ambiguity.

WCS allows _multiple_ coordinate systems to be specified for each data cube. Alternate coordinate systems are defined by specifying additional sets of WCS keywords, each set with a letter `A-Z` appended at the end. Keywords that may be used in this way are sometimes indicated with a suffix a, e.g., `CTYPEia` (see the FITS Standard Section 8.2.1). As an example, `CTYPE1B` specifies the type of coordinate `1` in coordinate system `B`.

In particular, multiple coordinate systems can be used to correctly describe data such as rasters, with one system describing the spatial-wavelength coordinate system (_x, y, lambda_), and another describing the temporal-spatial-wavelength coordinate system (_time, y, lambda_). Imaging observations scanning through the wavelength dimension could have a primary system describing (_x, y, lambda_) and a second coordinate system (_x, y, time_).

However, in many such cases it is simpler and more appropriate to use a single coordinate system with four coordinates, e.g., (_x, y, lambda, time_). This comes naturally if the observations are repeated and concatenated in time (i.e., resulting in a 4-dimensional data cube), but can also be used when scans are stored individually, (i.e., as 3-dimensional data cubes). In such cases, it is necessary to specify the number of coordinates with the keyword `WCSAXES``=4` in order to account for the time coordinate that is not represented by a dimension in the data cube.

For rotating FOVs in a time series, the table lookup algorithm for coordinates (see Paper III Section 6) must be used, with a joint table lookup of coordinates `HPLN-TAN`, `HPLT-TAN` and `UTC`. Since table lookup of WCS coordinates is performed with linear interpolation, it is normally possible to represent such a rotating FOV with a coordinate table that has size `(x,y,t)=(2,2,t)`, where `t` may be significantly smaller than the number of time steps in the time series. For highly non-linear rotation rates the indexed form of the table lookup algorithm may be used to vary the sampling of the FOV coordinates with time.

For observations (instruments) where the plate scale/pointing is derived from measurements of the apparent solar radius versus the physical size, the keywords `RSUN_REF` should be used to report the reference value for the physical radius used in the calculations (see Thompson 2010, Section 8).

For descriptions of distortions of coordinates in complex data sets, e.g., cavity errors, see [Appendix VI](#appendix-vi).

(3.2)=
## 3.2 WCS positional keywords and relative radial velocity

Ground based observatories must report their geographical location using the keywords `OBSGEO-X`, `OBSGEO-Y`, and `OBSGEO-Z`, implicitly stating that the observer is following Earth rotation (see Precision effects for solar image coordinates within the FITS world coordinate systems, Section 3; Paper III Section 7). In principle, the coordinates should be given in ITRF geocentric coordinates. However, for SOLARNET purposes, GPS coordinates are an acceptable proxy.

Earth-orbiting satellites must report their position through `GEOX_OBS`, `GEOY_OBS`, and `GEOZ_OBS`. Contrary to the `OBSGEO-X/Y/Z` keywords, these keywords do _not_ implicitly imply that the coordinates are fixed w.r.t. Earth’s rotation, but are otherwise identically defined (ITRF, but GPS is an acceptable proxy). For many observations, these keywords must be reported using the variable-keyword mechanism ([Appendix I](#appendix-i)) since the spacecraft might move considerably during the observation.

For deep space missions, the keywords `DSUN_OBS` (distance from Sun centre in metres), `HGLN_OBS` (longitude), and `HGLT_OBS` (latitude) must be used to report the instrument position in the Stonyhurst Heliographic system (see Thompson 2006, Sections 2.1 and 9.1). The distance from the Sun centre in astronomical units may be reported in `DSUN_AU` (in addition to `DSUN_OBS`). Note that the Solar B angle is identical to `HGLT_OBS`, and although it is a duplication of information, it may be reported also in `SOLAR_B0` for convenience.

If other coordinate systems or positional information are given for the observer position, they should follow the specifications in Thompson (2006), Sections 2.1 and 9.1.

For spectrometers (and for some narrow-band imagers), the radial velocity between the instrument and the Sun may be important. Unfortunately, WCS does not have a mechanism for specifying this without also correcting the wavelength scale to account for the Doppler shift (see Paper III, Section 7). Such a correction is not traditionally applied in FITS files within the solar physics community. To specify that no such wavelength correction has been done, `SPECSYS` must be set to `'TOPOCENT'` and `VELOSYS` must be set to `0.0`. In order to specify the observer’s radial velocity relative to the Sun, the non-WCS keyword OBS_VR (given in m/s) must be used (possibly as a variable keyword). Positive velocities are outward from the Sun (i.e., `OBS_VR`=_dr/dt_).

As mentioned also in Section 2, many keywords already established elsewhere but not mentioned in this document may apply. Such keywords should never be used in conflict with established use. In particular, see “Other sources of keywords with established use” under References. A few that are related to those defined in this section are: `SOLAR_P0` (apparent angle from observer location between celestial north and solar north), `SOLAR_EP` (apparent angle from observer location between celestial north and ecliptic north), `RSUN_ARC` (apparent photospheric solar radius in arc seconds), and `CAR_ROT` (Carrington rotation number for the reference pixel pointed to by `CRPIXja` values).

(4.0)=
# 4 Time-related WCS keywords

`DATE-BEG` _must_ be given, referring to the start time of the data acquisition in the time system specified by the `TIMESYS` keyword, which has the default of '`UTC`'. The `TIMESYS` value applies to all `DATE-` keywords, `DATEREF` (see Section 4.1), and several other date-valued keywords.

`DATE-END` may be given, referring to the end of data acquisition.

`DATE-AVG` may be used to give the average date of the observation. However, there is no unambiguous definition of the average when applied to observations with varying cadence or varying exposure times.

Note that we do _not_ recommend using the `DATE-OBS` keyword mentioned in the FITS Standard, since this is not explicitly defined there, and has a history of somewhat ambiguous use (see Paper IV).

The observer’s position may be important when comparing the times of observations from different vantage points – in particular when at least one of the observations is space based. Thus, the keywords `DSUN_OBS`, `HGLN_OBS`, and `HGLT_OBS` (Section 3.2) may be important w.r.t the timing of the observations.

(4.1)=
## 4.1 Specifying WCS time coordinates

The literature describing all the possible methods of specifying WCS time coordinates is very complex, but except in unusual circumstances, the following prescription should be sufficient:

`CTYPEia``='UTC'` should be used as the name of the WCS time coordinate. However, applications should also recognize the value `'TIME'` as having the same meaning, for historical reasons.

Also, `DATEREF` _must_ be set to the zero point of the WCS time coordinate. I.e., for pixels that have the `CTYPEia``='UTC'` coordinate equal to zero, the time is the value given in `DATEREF`. In most cases the values of `DATEREF` and `DATE-BEG` will be identical, but note that _according to the FITS standard,_ `DATE-BEG` _is not a default value_ for `DATEREF`, thus `DATEREF` may not be omitted. The existence of both keywords allows e.g., midnight to be used as a zero point for the time coordinate for multiple observations recorded during the following day, each having different values of `DATE-BEG`.

(5.0)=
# 5 Description of data contents

A description of the actual data contents is important for the interpretation of an observation. Such a description is also important for finding relevant observations in an SVO.

(5.1)=
## 5.1 Data type/units (BTYPE/BNAME/BUNIT)

The keywords `BTYPE`, `BNAME`, and `BUNIT` should be used to describe the nature of the data. The notation of mathematical expressions in `BUNIT` and `BNAME` should follow the rules in Table 6 of the FITS Standard, e.g. "`log(x)`" is defined as the common logarithm of `x` (to base 10).

`BUNIT` should be used to indicate the units of the values in the data cube.

`BTYPE` should be used to describe what the data cube itself represents. This keyword is not mentioned in any FITS standard document, but it is a natural analogy to the `CTYPEia` keywords used to indicate the WCS coordinate type. When possible, we recommend using the Unified Content Descriptors (UCD) version 1+ (see [References](#reference_list)) when specifying `BTYPE`, or gice the UCD description in a separate `UCD` keyword. It may be that the UCD scheme does not cover all data types encountered in solar observation. Thus, it may be necessary for the solar community to decide upon other values for this keyword. This is currently an unresolved issue.

`BNAME` may be used to provide a human readable explanation of the data contents. This keyword is not mentioned in any FITS standard document, but it is a natural analogy to the `CNAMEia` keywords used to provide additional description of the WCS coordinate.

(5.2)=
## 5.2 Exposure time, binning factors

The exposure time used in the acquisition of an Obs-HDU should be given in the keyword `XPOSURE` - not in `EXPTIME`. The reason why `EXPTIME` should not be used is that in _some cases_ it has been used for individual exposure times in summed multi-exposure observations, introducing an ambiguity. According to the recommendation in Paper IV, `XPOSURE` should always contain the _accumulated_ exposure time whether or not the data stems from single exposures or summed multiple exposures.

When the data are a result of multiple summed exposures with identical exposure times, the keywords `NSUMEXP` and `TEXPOSUR` can be used to indicate the number of summed exposures and the single-exposure time, respectively.

When the `XPOSURE` or `TEXPOSUR` values vary as a function of time or any other of the Obs-HDU’s dimension(s), the variable-keyword mechanism can be used to specify their exact values as a function of those dimensions (see [Appendix I](#appendix-i) for further details). This would typically be the case when Automatic Exposure Control is used - both `XPOSURE` and `TEXPOSUR` could vary as a function of time.

Note that if the data has been binned, the `XPOSURE` keyword should reflect the _physical_ exposure time, not the sum of exposure times of the binned pixels. Binning should be specified by the keywords `NBINj`, where `j` is the dimension number (analogous to the `NAXISj` keywords). E.g., for an observational data cube with dimensions `(x,y,lambda,t)` where 2x2 binning has been performed in the `y` and `lambda` directions (as is sometimes done with slit spectrometers), `NBIN2` and `NBIN3` should be set to 2. The default value for `NBINj` is 1, so `NBIN1` and `NBIN4` may be left unspecified.

In order to provide a simple way to determine the combined binning factor (for archive searches), the keyword `NBIN` should be set to the product of all specified `NBINj` keywords.

(5.3)=
## 5.3 Cadence

Cadence may be a very important search term. A meta-Obs-HDU may be used to report such attributes even if it is impossible to do so in the constituent HDUs ([Appendix III](#appendix-iii)).

The planned/commanded cadence (frame-to-frame timing between frames of the same type measured in seconds) should be reported in `CADENCE`. The average (actual) cadence should be reported in `CADAVG`.

The cadence _regularity_ is also important: The keywords `CADMAX` and `CADMIN` should be set to the maximum and minimum frame-to-frame spacing. `CADVAR` should be set to the variance of the frame-to-frame spacings.

Some instruments take interleaved observation series with a difference in cadence between different filters (“A” and “B”), e.g., AAABAAAB. For such a series, `CADENCE` for the A series should be the planned _median_ spacing between A exposures.

For e.g., on-going synoptic observation series stored with single exposures in separate files (thus separate HDUs) it may be impossible to use the Meta-observation mechanism. The `CADENCE` keyword should be set to the planned series' cadence. The rest of the keywords should be set based on the available history of the synoptic series.

(5.4)=
## 5.4 Instrument/data characteristics etc

In order to characterise the spectral range covered by an Obs-HDU, the keywords `WAVEMIN` and `WAVEMAX` should be used to specify the minimum and maximum wavelengths.

The magnitude of the wavelength related keywords mentioned in this section (`WAVExxx`) must be specified in `WAVEUNIT`, given as the power of 10 by which the metre is multiplied, e.g., `WAVEUNIT``=-9` for nanometre. We recommend that `WAVEUNIT` corresponds to the `CUNITia` value of the WCS wavelength coordinate, if any, e.g., if `CUNITia``='Angstrom'` then `WAVEUNIT``=-10`.

`WAVEREF` should be set to `'air'` or `'vacuum'` to signal whether wavelengths are given for air or vacuum. We recommend that `WAVEREF` corresponds to the `CTYPEia` value of the WCS wavelength coordinate, if any. E.g., if `CTYPEia``='AWAV'` then `WAVEREF``='air'`.

For spectrometers, the `WAVEMIN`/`WAVEMAX` values represent the range of wavelengths covered by the Obs-HDU. If the file contains multiple readout windows, the wavelength coverage of the entire file may be reported in `WAVECOV``='(<WAVEMIN1>-<WAVEMAX1>, <WAVEMIN2>-<WAVEMAX3>, …)'`

For filter images, the definition is somewhat up to the discretion of the pipeline constructor since effective response curves are never a perfect top-hat function. Bear in mind that these two keywords are primarily meant to be used for search purposes. E.g., if someone wants an observation covering a specific wavelength lambda, the search can be formulated as `“WAVEMIN < lambda < WAVEMAX”`. In other words, it might be wise to include more than the “intended” or “nominal” min/max wavelengths of a filter: sometimes parts of an extended tail should be included if it covers a potentially interesting emission line that is normally very weak but may be strong under certain conditions. We suggest that the wavelengths at which the response function is 0.1 times the peak might be a good choice, unless other considerations make other choices more appropriate. This should be based on a measured response function if available – otherwise it should be based on a design specification or theoretical basis. We reiterate, though, that the criteria are up to the discretion of the pipeline designers. The criteria used to set these keywords should in all cases be specified in the keywords’ comment.

For filter images, the `WAVELNTH` keyword may be set to the “characteristic wavelength” at which the observation was taken. For EUV imagers, this keyword typically identifies the most prominent emission line in the bandpass. For a spectrometer `WAVELNTH` might also be the middle of the wavelength range of the HDU, but we leave the exact definition up to the pipeline designers.

In addition, the keyword `WAVEBAND` may be used for a human-readable description of the waveband, typically the (expected) strongest emission/absorption line in HDUs containing spectrometer observations (or specifying the continuum region), or the most dominant contributing line in filter images.

For radio observations, `BNDCTR` may be used instead of `WAVELNTH` to specify a corresponding frequency in Hz.

For filter observations where a more thorough specification of the response curve is required for a proper analysis or for search purposes, the variable keyword `RESPONSE` may be used – see [Appendix I](#appendix-i).

The `RESPONSE` keyword should also be used for spectrometers where there are significant variations in the response across the dataset.

If the data has already been corrected for a variable response, the response function that has been applied should instead be given in the variable keyword `RESPAPPL`.

For spectrometric data, the resolving power R should be given in the keyword `RESOLVPW`. For slit spectrometers, the slit width in arc seconds should be given in `SLIT_WID`.

(5.4.1)=
## 5.4.1 Polarimetric data reference system

Different Stokes values are normally stored together in a _single_ extension, with a `STOKES` dimension and an associated `STOKES` coordinate to distinguish between the different values `(I/Q/U/V or RR/LL/RL/etc)`. The `STOKES` coordinate should vary along the `STOKES` dimension according to Table 29 in the FITS Standard. Pixels containing I, Q, U, and V values should have `STOKES` coordinates 1, 2, 3, and 4, respectively. If different Stokes values are stored in different extensions or in different files, the `STOKES` coordinate should still be specified - either as a “phantom” WCS coordinate without an associated data dimension (i.e., `WCSAXES > NAXIS`) or as a regular coordinate for a singular data dimension.

Existing conventions for specifying the _reference system_ for Stokes vectors use celestial coordinates (`RA/DEC`), but for Solar observations this is not practical. Thus, we define here that SOLARNET-compliant FITS files should use a right-handed reference system _(x, y, z)_ with the _z_ coordinate oriented either parallel or antiparallel with the line of sight towards the observer. The axes must be explicitly specified by the keyword `POLCCONV` in the form `'(+/-x, +/-y, +/-z)'` where `x`, `y`, and `z` are valid WCS coordinate names. E.g., `POLCCONV``='(+HPLT,-HPLN,+HPRZ)'` means that the reference system’s _x_ axis is parallel to the `HPLT` axis (Solar North), and _y_ is _antiparallel_ to the `HPLN` axis, with _z_ pointing towards the observer.

If the polarimetric reference frame is not aligned with any set of WCS coordinate names, a rotation of the reference frame given in `POLCCONV` can be specified in `POLCANGL`. The rotation, specified in degrees, should be applied to the `POLCCONV`-specified system around its third axis. The rotation is counter-clockwise as seen from a point with a positive third-axis coordinate value, taking the sign from `POLCCONV` into account. I.e., specifying a positive angle with `POLCCONV``='(…, …, +HPRZ)'` specifies a counter-clockwise rotation as seen from Earth, whereas with `POLCCONV``='(…, …, -HPRZ)'` would specify a clockwise rotation as seen from Earth.

(5.5)=
## 5.5 Quality aspects

Many quality aspects of ground-based observations change rapidly, even from one exposure to the next. Keywords that describe such quality aspects must therefore often use the variable-keyword mechanism to specify the time evolution of such values, see [Appendix I](#appendix-i). This mechanism may be used to specify quality-related values for single exposures, average or effective values for composite images, while also allowing an average or effective scalar value to be given in the header.

Until now, there has been little effort in order to characterise quality aspects of ground-based observations in a manner that is _consistent_ between different telescopes, and even between different setups at the same telescope. In FITS files from ESO (European Southern Observatory), the keyword `PSF_FWHM` is used to give the full width at half maximum in arc seconds for the point spread function. However, this quantity is generally not available for solar observations. Some adaptive optics systems, however, may record parameters like the atmospheric coherence length r<sub>0</sub>. If available, the value of r<sub>0</sub> should be stored in the keyword `ATMOS_R0`. Since there are multiple ways of measuring this value, its only use should be to reflect the quality of the observing conditions whenever the measurements are performed in the same (or similar enough) way.

If you have suggestions for consistent methods of measuring parameters describing the spatial resolution of observations (or a proxy for it), please add an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues), so that we can include this method in a later version of the document.

The keyword `AO_LOCK` should be used to indicate the status of any adaptive optics. When specified for individual exposures, the value should be either 0 or 1, but as mentioned above, averages may also be specified as appropriate.

The keyword `AO_NMODE` should be used to indicate the number of adaptive optics modes corrected. As mentioned above, averages may also be specified as appropriate. The type of the modes (e.g., Zernike, Karhunen-Loeve, etc.) should be given in the keyword comment.

The keyword `FT_LOCK` is used to indicate the status of any feature tracking `FT_LOCK``=0` (no feature tracking lock) or `FT_LOCK``=1` (feature tracking lock) for individual exposures, with appropriate averages as mentioned above.

The keyword `ROT_COMP` should be set to 1 if solar rotation compensation was in effect during the observation <span class=new>*and is accounted for in the WCS coordinates*. If rotation compensation was in effect *but is not reflected in the WCS coordinates*, it should be set to 2. If rotation compensation was not in effect, it should be set to 0 or be absent</span>. If `ROT_COMP``=1` the keyword `ROT_MODL` should be set to specify the rotation model used for rotation compensation[^footnote-4]. It can refer to specific, predefined models such as `ALLEN` (Allen, Astrophys. Quantities, 1979), `HOWARD` (Howard _et al._), `SIDEREAL`, `SYNODIC`, `CARRINGTON`, `SNODGRASS` or `aaa.a` (arcseconds per hour). See also the SolarSoft routine `diff_rot.pro`. If other models have been used, please create an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues), or set `ROT_MODL` to `FORMULA`, and specify the formula in the keyword `ROT_FORM`. The formula is meant to be human-readable, not machine readable (e.g., `'A sin(…)'`), using parameter names that are common within your community. Header keywords may be used directly in the formula, as can coordinates (e.g., HPLT or HPLT-TAN). Since both keywords and coordinate names may contain dashes, the formula should always have spaces surrounding actual minus signs. An explanation in the comments may be useful.

[^footnote-4]: This might be important when comparing observations where cross-correlation cannot be used for alignment -e.g., coronal observations vs. photospheric observations. In such cases, different rotation models might cause a drift between the two. The information in this keyword can be used to prevent misunderstandings and misinterpretations in in such situations.

If other relevant keywords seem necessary, we recommend using keywords starting with `'ROT_'`, but please contact us as well.

`ELEV_ANG`: This keyword should be used to quote the telescope’s elevation angle at the time of data acquisition, in degrees.

In some cases, lossy compression has been applied to the data. Depending on the type of compression, different quality aspects will be introduced that should somehow be specified. Since any significant on-board processing should be considered as a processing step in the pipeline, lossy compression may be listed using the `PRxxxxn` keywords described in Section 8.

However, for searching and sorting purposes it would be useful to have a generic numeric keyword describing the loss of quality due to lossy compression.

`COMPQUAL` could therefore be set to a number between 0.0 and 1.0, where 1.0 indicates lossless compression (if any) and 0.0 indicates “all information is lost”. In practice, however, the actual value is not crucial, as long as a higher value corresponds to a higher data quality. If there is a choice between different compression algorithms for this instrument, the name of the algorithm should be given in `COMP_ALG` – starting with either `'Lossy'` or `'Lossless'`, then typically a concatenation of all instrument-specific compression-related keywords, separated with slashes.

<span class=new>`SIGMADAT`: Normally a formula specifying how to calculate the standard deviation {math}`\sigma` of each pixel. The formula should be given as a human-readable string, e.g., `'sqrt( data^2 + (2*GAIN*XPOSURE)^2 )'`, where `data` is the pixel value. Header keywords (e.g., `XPOSURE`) may be used directly in the formula. Since keyword names may contain dashes, *actual minus signs in the formula must be surrounded by spaces*. To increase the readability and interpretability of the formula, try to avoid using "magical constants" (i.e., add instead descriptive keywords in the header to use in the formula, with comments). If formula parameters are not constant for the entire data cube (e.g., for different readout quadrants), variable keywords can be used ([Appendix I](#appendix-i)). Even the formula itself can be specified as a pixel-to-pixel variable keyword ([Appendix I-b](#appendix-ib))</span>

<span class=new>If it's not practical to give a formula at all (e.g., if the sigma values as a function of data is discontinuous), it may be specified as a curve in a separate extension using an `EXTNAME` name that starts with `'CURVE:'`, e.g., `SIGMADAT``='CURVE:SIGMA-TABLE'`. The contents of this extension should be a data cube with dimension `[2,n]`, functioning as a lookup table where `(1,*)` are data values and `(2,*)` are the corresponding {math}`\sigma` values. The table is subject to linear interpolation. The {math}`\sigma` values may also be specified on a pixel-by-pixel basis.</span>

<span class=new>If it is necessary to specify {math}`\sigma` directly for each individual pixel, values can be specified in an extension with an `EXTNAME` that starts with `'VALUES:'`, e.g., `SIGMADAT``='VALUES:SIGMA-VALUES'`. The extension should have the same dimensions as the original data.</span>

`OBS_LOG`: Location of the log file that is relevant to this observation, if available, given as a URL.

`COMMENT`: May be used to include the relevant parts of the `OBS_LOG`, and any other relevant comments about the HDU that may be useful for the interpretation of the data.

(5.6)=
## 5.6 Data statistics

It may be useful to have statistics about the data cube of a Obs-HDU in order to search for “particularly interesting” files (or to filter out particularly _uninteresting_ files for that matter).

`DATAMIN` – the minimum data value

`DATAMAX` – the maximum data value

`DATAMEAN` – the average data value

`DATAMEDN` – the median data value

`DATAPnn` – the nn percentile (where `nn` is e.g., `01, 02, 05, 10, 25, 50, 75, 90, 95, 98, and 99`).

`DATANPnn` – `DATAPnn/DATAMEAN`, i.e., normalized percentiles

`DATARMS` – the RMS deviation from the mean, sqrt( sum( (x-avg(x))^2 )/N )

`DATANRMS` – `DATARMS/DATAMEAN`, i.e., normalized RMS.

`DATAMAD` – the mean absolute deviation, avg( abs( x-avg(x) ) )

`DATANMAD` – `DATAMAD/DATAMEAN`, i.e., normalized MAD

`DATAKURT` – the kurtosis of the data

`DATASKEW` – the skewness of the data

Note that the calculation of these keywords should be based only on pixels containing actual observational data – not including e.g., padding due to rectification, etc.

(5.6.1)=
## 5.6.1 Missing and saturated pixels, spikes/cosmic rays, padding, etc

In some data sets, the data in the HDU may be affected by missing/lost telemetry, acquisition system glitches, cosmic rays/noise spikes, or saturation, hot/cold pixels etc. Some keywords are useful to find/exclude files based on how many such pixels there are. In order to allow such searches, the following keywords should be used:

`NTOTPIX` – the number of _potentially_ usable pixels: the number of data cube pixels minus `NMASKPIX`

`NLOSTPIX` – the number of lost pixels due to telemetry/acquisition glitches

`NSATPIX` – the number of saturated pixels

`NSPIKPIX` – the number of identified spike pixels

`NMASKPIX` – the number of dust-affected/hot/cold/padded pixels etc.

`NAPRXPIX` – the number of pixels with approximated values (used by e.g., SolO/SPICE)

`NDATAPIX` – the number of usable pixels: `NTOTPIX - NLOSTPIX - NSATPIX - NSPIKPIX`

Corresponding percentages relative to `NTOTPIX` should be given in `PCT_LOST`, `PCT_SATP`, `PCT_SPIK`, `PCT_MASK`, `PCT_APRX` and `PCT_DATA`.

It is strongly recommended that this naming pattern is followed whenever there is a need to specify further “classes of pixels”. I.e., to introduce the pixel class `'SOME'`, `PCT_SOME` should be used to give the corresponding percentage relative to `NTOTPIX`. Analogously, the associated list of pixels (see below), should be named `SOMEPIXLIST`.

(5.6.2)=
## 5.6.2 Explicit listing of missing, saturated, spike/cosmic ray pixels etc

Bad pixels may be handled in one of three ways: they can be left untouched, they can be filled with the value of `BLANK` (integer-valued HDUs) or _NaN_ (floating-point-valued HDUs), or they can be filled in with estimated values.

For some purposes, it may be useful to keep lists of individual bad pixels or ranges of bad pixels using the pixel list mechanism, see [Appendix I-d](#appendix-id). This is especially important when the pixels have been filled in with estimated values, storing the original values in the pixel list. Pixel lists that flag individual lost, approximated, saturated, spike or masked pixels, should have `EXTNAME`s equal to `LOSTPIXLIST`, `APRXPIXLIST`, `SATPIXLIST`, `SPIKPIXLIST`, or `MASKPIXLIST` respectively. Original values (when appropriate) should be given in the pixel list’s attribute column with `TTYPEn``='ORIGINAL'` – see [Appendix I-d](#appendix-id). for details. For cosmic ray/spike detection, a confidence level (between 0.0 and 1.0) may also be given in an attribute column with `TTYPEn``='CONFIDENCE'`. In order to ensure unique `EXTNAME`s for pixel lists belonging to different Obs-HDUs, the pixel list `EXTNAME`s may have a trailing “tag”, see [Appendix I-d](#appendix-id). Pixel lists with other `EXTNAME`s than `LOSTPIXLIST` etc. may of course be used for other purposes, e.g., storing the pixel indices and classification of sunspots, the latter stored as a string valued attribute.

(6.0)=
# 6 Metadata about affiliation, origin, acquisition, etc

The keywords in this section describe metadata regarding the origin, acquisition, and affiliation of the data. Although not generally required for the _use_ of the data, such metadata are very useful w.r.t. e.g., searching, grouping, counting, and reporting. Some of the keywords will not make sense for all data sets, because the nature and nomenclature of the observational scenarios vary. In such cases, leave them out. Also, some of the keywords will have different meanings within different settings, in many cases based on tradition.

We therefore refrain from giving explicit instructions on the usage of many of the keywords. An SVO should allow searching on such keywords by asking for “observations where `PROJECT``=xxx`”, but it should also be possible to search for “observations where `xxx` occurs in any of the keywords mentioned below”.

In general, all keywords below may contain comma-separated lists when necessary. In some cases, it may be a good idea to use both the full name and an acronym.

We _strongly_ recommend that all such “free-text” keywords are filled in from lists of predefined texts, strictly controlled by each individual pipeline/instrument team. Experience has shown that free-text fields will be filled in incredibly inconsistently, even the writer’s own name. Of course, it would be even better if a community-wide service could be established to homogenise such controlled lists, but this may never happen.

`PROJECT`: Name(s) of the project(s) affiliated with the data

`MISSION`: Typically used only in space-based settings (e.g., the SOHO or STEREO mission)

`OBSRVTRY`: Name of the observatory

`TELESCOP`: Name of the telescope.

`TELCONFG`: Telescope configuration.

`INSTRUME`: Name of the instrument.

`CAMERA`: Name of the camera (`CAM-xxxx` is recommended for other camera keywords).

`GRATING`: Name of the grating used (when there are more than one available).

`FILTER`: Name(s) of the filter(s) used during the observation.

`DETECTOR`: Name of the detector.

`OBS_MODE`: A string (from a limited/discrete list) uniquely identifying the mode of operation.

`OBS_DESC`: A string describing the observation, e.g., “Sit and stare on AR10333”. Content sources may be e.g., observation logs. Should be identical to `OBSTITLE` when no more suitable value is available.

`OBSTITLE`: A more generic/higher-level description, e.g., “Flare sit-and-stare”, “High cadence large raster”). The contents will often correspond to `OBS_MODE`, though not necessarily as a one-to-one relationship. Used by IRIS and SPICE, corresponds to Hinode `OBS_DEC`. Should be identical to `OBS_DESC` or `OBS_MODE` when no more suitable value is available.

`SETTINGS`: Other settings – numerical values can be given as `'parameter1=n, parameter2=m'`.

`OBSERVER`: Who acquired the data.

`PLANNER`: Observation planner(s).

`REQUESTR`: Who requested this particular observation.

`AUTHOR`: Who designed the observation

`CAMPAIGN`: Coordinated campaign name/number, including instance number, when applicable.

Note also this catch-all keyword:

`DATATAGS`: Used for any additional search terms that do not fit in any of the above keywords.

(7.0)=
# 7 Grouping

_It is very important for an SVO to be able to group search results in a meaningful way!_

E.g., if a search matches 1000 Obs-HDUs, but they are part of only 5 different observation series, it makes sense to have a grouping mechanism to collapse the result listing into only 5 lines, showing some form of summary of the underlying Obs-HDUs for each series.

(7.1)=
## 7.1 Pointing ID _separates_ observations into groups

To make such grouping work, the concept of a “pointing id” has proven to be useful in e.g., the Hinode archive – it serves to _separate_ otherwise identical observations into groups in a logical way.

We therefore introduce the keyword `POINT_ID`, to be given a new, unique string value (e.g., a string giving the date and time of the repointing) every time the telescope is _significantly repointed_ - not counting feature tracking or rotation compensation.

Note that changes in the size of the FOV is not considered a repointing. E.g., an alternating series of large-FOV and small-FOV observations should share a single `POINT_ID` value, even if the FOVs are not centred on the same spot – the small-FOV and large-FOV observations may be sorted into separate, parallel groups based other characteristics given by keywords defined below.

Thus, `POINT_ID` is used to _separate_ files that should _not_ be lumped together in a group because doing so would disguise or misrepresent “what has been observed”.

The exact criteria used for changing the `POINT_ID` value are left up to the pipeline designers/observers, but _we would like to stress the importance of this particular keyword for SVO/archive purposes. Without it, the archive may have no other option than to list your observations with one line per file/Obs-HDU!_

Planning tools/databases are often good sources for of `POINT_ID` values, but with some processing some information may be available from automated logging of telescope orientation, etc.

Even fixed-pointing instruments should use `POINT_ID` to e.g., separate multiple contiguous sequences with breaks in between.

(7.2)=
## 7.2 Further separating observations with identical pointing ID

Grouping observations solely on the basis of their `POINT_ID` values will lump together observations regardless of other characteristics such as filters, exposure times, slit widths, etc. In order to separate such disparate observations, further information needs to be taken into account. As an example, grouping on the basis of a concatenation of the values of `POINT_ID`, `CAMERA`, `DETECTOR`, `GRATING`, `FILTER`, `SLIT_WID`, `XPOSURE`, `OBS_MODE`, `SETTINGS`, `NBIN1`, `NBIN2`, `NAXIS1`, and `NAXIS2` would in most cases ensure that only completely identical observations are grouped together (if `XPOSURE` is a measured quantity with slight variations due to e.g., shutter speed variance it should be left out). Exactly which keywords should be used is of course highly instrument dependent.

For other purposes, however, a coarser grouping might make more sense. E.g., omitting `FILTER`, `SLIT_WID`, and `XPOSURE` may still make sense in an archival context if showing a single search result line with a single image gives the user a good (enough) idea of what the observation group contains (e.g., a sunspot or no sunspot). Thus, a hierarchy of groupings can be established, from fine-grained to coarse.

To guide archive designers in the process of presenting grouped observations, we introduce the keywords `SVO_SEPn`, with `n` spanning from `1` to `5`. `SVO_SEP1` should have a comma-separated list of keywords giving the most fine grained grouping, and `SVO_SEP5` should have a comma-separated list of keywords giving the coarsest sensible grouping. Normally, the first keyword should be `POINT_ID`, and it may be the only keyword. Not all `SVO_SEPn` keywords need to be defined, but they should be populated starting with `SVO_SEP1`.

Examples:

```none
SVO_SEP1= 'POINT_ID,INSTRUME,DETECTOR,FILTER,NBIN' / Most fine grained separation
SVO_SEP2= ‘POINT_ID,INSTRUME,DETECTOR,FILTER’ / Img. shows target even w/binning
SVO_SEP3= ‘POINT_ID,INSTRUME,DETECTOR’ / Target identifiable in all filters
SVO_SEP4= ‘POINT_ID,INSTRUME’ / Still useful
```

Note that the `SVO_SEPn` keywords are only _guidelines_ for archive designers. Typically, an archive will also separate groups by data level if it contains more than a single level.

(7.3)=
## 7.3 Group ID ties together logical groups of observations

`SVO_GRP` may be used to achieve the opposite, to tie observations _together_ even if they have different `POINT_ID`s and/or have other differing characteristics. Heuristically, a shared value for `SVO_GRP` signals that “if you are interested in this observation, you are probably interested in all of these observations (with the same `SVO_GRP` value)”.

(7.4)=
## 7.4 Mosaics

For mosaic observations, the keyword `MOSAICID` can be used to tie individual observations together.

(8.0)=
# 8 Pipeline processing applied to the data

The concept of “data level” is often used to label data with a particular degree of processing, from raw data up to complex data products.

However, definitions of data levels are extremely instrument-/mission-/pipeline-dependent, and not very useful in terms of explaining what processing has been applied. This concept is useful, however, to ensure that files with different processing level have unique file names. For this reason, the keyword `LEVEL` may be used, as a string value to capture sub-levels such as quick-look versions.

`VERSION` should be set to the _processing version of the file_, an integer that should be increased whenever a reprocessing is performed in order to improve the data set (e.g., with a better flat-field, better detection of cosmic rays, more complete telemetry, etc). The version numbers in files published through an SVO may increase by more than one for each new published “generation”, allowing the use of intermediate values for internal/experimental use.

`ORIGIN` should be set to a character string identifying the organization or institution responsible for creating the FITS file. DATE should be set to the date of creation of the FITS file.

<span class=new>`PARENTXT` (parent extension) should be used to reference the extension(s)/files from which the current extension has been created. It will typically be a comma-separated list of external extension references, i.e., a list of relative paths, filenames and extension names such as:</span>

```none
PARENTXT = '../level1/obs1_level1.fits;Window A'
```

<span class=new>For parent files that are not FITS files or lack an EXTNAME (for the primary HDU), the semicolon and extension name can be omitted. E.g.:</span>

```none
PARENTXT = '../telemetry/20250102-000.tlm, /level1/obs1_level1.fits;Window A'
```

<span class=new>When concatenating a series of many files (e.g., converting repeated rasters to a movie) with a common filename marker, the wildcard syntax may be useful (see [Appendix VII](#appendix-vii)).
For Level P data, which have `OBS_HDU``=2`, the extensions referenced in `PARENTXT` should also be used as an additional source of metadata, as if the `PARENTXT` extension was the primary HDU and the `INHERIT` convention was in use [FITS Header Inheritance Convention](https://fits.gsfc.nasa.gov/registry/inherit/fits_inheritance.txt) (see [References](#reference_list)).</span>

In addition to the `LEVEL`, `VERSION`, `PARENTXT` and `ORIGIN` keywords, we recommend that some additional keywords are used in order to indicate the processing steps that has been applied to the data. The four keywords described in Section 8.1 may be used instead of or in addition to the more complex set of keywords described in Section 8.2.

(8.1)=
## 8.1 Basic description of processing software

The name and version of the processing software should be specified by those of the following keywords that might apply:

```none
CREATOR = 'ZUN_MOMF_PIPELINE' / Name of software pipeline that produced the FITS file`
VERS_SW = '2.5'       / Version of software applied`
HASH_SW = 'a7ef89ad998ea7feef4bbc0bbc1bbc2bbc3bbc4' / Commit hash of software applied`
VERS_CAL = '2.4'       / Version of calibration pack applied
```

In addition, `PRSTEPn` should specify the nature of the processing steps, if any, that has been applied to the data. Each `PRSTEPn` may contain a comma separated list if multiple processing steps are inseparable. The number n specifies the step number and should reflect the order in which the steps have been performed, e.g.:

```none
PRSTEP1 = 'FIXED-PATTERN,FLATFIELDING' / First two (inseparable) processing steps`
PRSTEP2 = 'CALIBRATION' / Second processing step
PRSTEP3 = 'DISTORTION-CORRECTION' / Third processing step
```

Below is a list of recommendations for descriptions of processing steps. If desirable, further specifications may be added, e.g., instead of `'LINE-FITTING'` one may want to use `'GAUSSIAN-LINE-FITTING'` versus `'VOIGT-LINE-FITTING'`. Note that distortion corrections come in two flavours: applied to the data (regridding) or applied to the coordinates. In the latter case, `COORDINATE` should be a part of the processing step description. If you need to add to this list, please create an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues).

```none
ATMOSPHERIC-INVERSION
BIAS-CORRECTION
BINNING
CALIBRATION
CEILING
COMPRESSION
CONCATENATION
DARK-SUBTRACTION
DEMODULATION
DEROTATION
DESPIKING
DESTRETCHING
EDGE-DETECTION
FILTERING
FIXED-PATTERN-REMOVAL
FLATFIELDING
FLOORING
LINE-FITTING
MOMFBD
MULTIPLICATION
PIXEL-FILLING
PIXEL-LEVEL-OFFSET-SUBTRACTION
RADIOMETRIC-CALIBRATION
ROUNDING
SHACK-HARTMANN-DECONVOLUTION
SPATIAL-ALIGNMENT
SPATIAL-COORDINATE-CORRECTION
SPATIAL-COORDINATE-CORRECTION-X
SPATIAL-COORDINATE-CORRECTION-Y
SPATIAL-COORDINATE-DISTORTION-CORRECTION
SPATIAL-DISTORTION-CORRECTION
SPECKLE-DECONVOLUTION
SPECTRAL-ALIGNMENT
SPECTRAL-COORDINATE-CORRECTION
SPECTRAL-COORDINATE-DISTORTION-CORRECTION
SPECTRAL-DISTORTION-CORRECTION
STOKES-INVERSION
SUBTRACTION
SUMMING
TELEMETRY-PARSING
THRESHOLDING
WFS-DECONVOLUTION
```

(8.2)=
## 8.2 Detailed description of all processing steps

Each processing step may be described in further detail using some or all of the following keywords in addition to `PRSTEPn`: `PRPROCn`, `PRPVERn`, `PRMODEn`, `PRPARAn`, `PRREFn`, `PRLOGn`, and `PRENVn`.

Libraries used in processing step `n` may be described using some or all of the keywords `PRLIBna`, `PRVERna`, `PRHSHna`, and `PRBRAna`, where a is an optional but highly recommended letter `A-Z` to signal that the keyword describes a library, not the main procedure, and to distinguish between different libraries. E.g.:

```none
PRSTEP1 = 'MOMFBD ' / Processing step type
PRPROC1 = 'zun_momf.pro' / Name of procedure performing PRSTEP1
PRPVER1 = 1.5 / Version of procedure PRPROC1
PRMODE1 = 'BALANCED' / Processing mode of PRPROC1
PRPARA1 = 'ITER=5,MANUAL=1' / List of parameters/options for PRPROC1
PRREF1 = '<miss.influencer@esa.int>' / Factors influencing PRSTEP1
PRLOG1 = ' % Program caused arithmetic error: Integer divide by 0' / PRPROC1 log
PRENV1 = ' Kernel: Linux &'
CONTINUE ' Kernel release number: 3.10.0-1160.36.2.el7.x86_64 &'
CONTINUE ' OS: Red Hat Enterprise Linux Server release 7.9 (Maipo) &'
CONTINUE ' CPU: Intel(R) Xeon(R) CPU E5-2630L v4 @ 1.80GHz &'
CONTINUE ' IDL 8.5 (Jul 7 2015), memory bits: 64, file offset bits: 64 &'
CONTINUE '' / Processing environment of PRSTEP1
PRLIB1A = 'ZUNRED ' / Software library containing PRPROC1
PRVER1A = 32214 / Version of PRLIB1A
PRHSH1A = 'a7ef89ad998ea7feef4bbc0bbc1bbc2bbc3bbc4' / GIT commit hash for PRLIB1A
PRBRA1A = 'production' / GIT/SVN repository branch of PRLIB1A
PRLIB1B = 'SSW/vobs/ontology/idl/gen_temp,SSW/packages/sunspice/idl/atest,SSW/&'
CONTINUE 'so/spice/idl/atest,SSW/vobs/gen/idl,SSW/soho/gen/idl/util,SSW/gen/i&'
CONTINUE 'dl_libs/astron/coyote’ / Software library containing PRPROC1
PRVER1B = 59549 / Modified Julian date of last mirroring of PRLIB1B
```

In this example, the `zun_momf.pro` routine is part of the `ZUNRED` library and relies on SolarSoft library routines. If further libraries had been used in processing step 1, they would be specified in `PRLIB1B`, etc. Libraries should be listed in the order they appear in the path. Unfortunately, some libraries such as SolarSoft contain internal routine shadowing, in which case each conflicting sub-package must be listed as a separate library in the order they appear in the effective IDL path, i.e., in the system variable `!PATH`[^footnote-5].

[^footnote-5]: For SolarSoft, the correct order in which these sub-packages should be listed may be found by tracing the effects on `!PATH` from the beginning (the `$SSW_INSTR` environment variable) to the end, taking into account the effects of `rm_path` and `add_path` statements.

If a single procedure performs multiple steps, it is ok to list each step separately, using the same value in e.g., `PRPROC1` and `PRPROC2`, but different values for `PRSTEP1` and `PRSTEP2`.

The version keywords `PRPVERn` and `PRVERna` should be numerically increasing with increasing maturity of the pipeline. When using libraries with no (numeric) version numbers, the Modified Julian Day (MJD) of the time the library was last mirrored/changed could be used as a version number. Note that for git repositories, it is possible to construct a consistently increasing version number by counting the total number of commits in a fiducial master repository. If none of the above is available, the MJD of the processing itself may be used, implying that the processing uses the latest version available at that date.

`PRHSHna` is a convenience keyword to easily find the exact git commit for a library that has been used. Note that _it does not replace_ `PRVERna`, because `PRHSHna` is not a number that increases with the maturity of the libraries (but such a number can be constructed, see above).

`PRMODEn` is meant for pipelines that may be run with different trade-offs between e.g., signal to noise ratio versus spatial resolution or contrast. This should already be apparent from the other keywords, but `PRMODEn` provides a much simpler way of identifying data processed in a particular way (e.g., `“BALANCED”` or `“HIGH CONTRAST”`). Note that a single observation may be registered multiple times in an SVO with different values of `PRMODEn` - but then a `PRMODEn`-specific identifier in the file name is necessary in order to ensure uniqueness.

The `PRPARAn` keyword can be used in different ways:

1. As a plain comma-separated listing of parameters and their values, signalled by the first character matching the regular expression `'[A-Za-z_$]'`
2. As a JSON string, signalled by the first character being an opening curly bracket
3. As an XML specification, signalled by the first character being a `'<'`
4. As the `EXTNAME` of an ASCII table, signalled by the first character being a `'['`

When `PRPARAn` is used as a reference to an ASCII table, the extension's first three columns should be the parameter name, the parameter value, and an optional comment. It is allowed to use a single ASCII table extension for all processing parameters, but this is of course only possible if all parameter names of all processing steps are distinct. Also, it is recommended to repeat _all_ `PRxxxxn` keywords from the Obs-HDU in the header of the ASCII table extension, so that the entire processing history of the data can be seen from that header alone. When parameters are given in separate extensions for each step, it may be less confusing if only the `PRxxxxn` keywords for that particular step is included.

For plain parameter lists, IDL parameter syntax must be used. For ASCII table extensions, values should be specified with regular FITS syntax. For ASCII table extensions, complex values can be written with parentheses containing the real and imaginary parts. Array-valued parameters can be written as a comma-separated list in square brackets in both of these formats.

`PRENVn` can be used to specify the operating environment of the pipeline such as the hardware (CPU type) and the operating system type/version, compiler/interpreter versions, compiler options, etc.[^footnote-6] The default value of a `PRENVn` keyword is the value of `PRENVn` in the previous processing step, so for a pipeline that has been run from beginning to end in a single environment, only `PRENV1` will have to be specified.

[^footnote-6]: This may seem like overkill, but there are instances where e.g., OS versions have mattered, see https://www.i-programmer.info/news/231-methodology/13188-python-script-invalidates-hundreds-of-papers.html, leading to papers being retracted/corrected. Also, for the BIFROST code, on some  particular platform a particular CPU instruction optimization has to be turned off with a compiler flag to produce correct results.In the SPICE project it was observed that calculations of mean, variance, skewness, and kurtosis using the built-in IDL method `MOMENT()` differed by as muchas 0.6%, 1.6%, 2.4% and 3%, respectively! This may be very significant if such parameters are used to make cuts in a data set.

`PRREFn` is a catch-all keyword that can be used to specify other factors/inputs influencing a processing step, e.g., references to images used for pointing adjustments. `PRREFn` may be a comma separated list of multiple factors/inputs[^footnote-7].

[^footnote-7]: In order to differentiate between very different factors influencing a processing step, `PRREFnx` maybe used, where `x` is a letter A-Z.E.g., `PRREF1A` may list files and `PRREF1B` may list names of people.

`PRLOGn` can be used to include a processing log in case messages/warnings from the processing may be of importance.

For some data sets, it may be desirable to include information about how the calibration data has been created/processed (e.g., acquisition of flat fields/dark images). In such cases, the same mechanism should be used, even though the observational data in the HDU is not altered by that processing in itself. The processing steps for the calibration data should have a lower n than those steps that use the calibration data (e.g., `PRSTEP1='CALIBRATION-PREPARATION'` and `PRSTEP2='CALIBRATION'`).

(9.0)=
# 9 Integrity and administrative information

The `DATASUM` and `CHECKSUM` keywords (see the [Checksum Keyword Convention](http://fits.gsfc.nasa.gov/registry/checksum.html)) should be set in all HDUs to allow a check on whether the data file has been modified from the original or has become corrupted. However, their values in a Meta-HDU (see [Appendix III](#appendix-iii)) will be recomputed when constituent HDUs have been combined into a single HDU (after checking the constituent HDUs `DATASUM` and `CHECKSUM`).

`INFO_URL` should point to a human-readable web page describing “everything” about the data set: what it is, how to use it, links to e.g., user guides, instrument/site/telescope descriptions, descriptions of caveats, information about data rights, preferred acknowledgements, whom to contact if you have questions, and repositories of observing/engineering logs.

Upon ingestion of (meta)data into an SVO, the material pointed to by `INFO_URL` and `OBS_LOG` (Section 5.5) might be “harvested” and preserved in such a way that it is possible to retrieve a copy even if the original source is no longer available. It might be possible for an SVO to recursively harvest pages/documents and even auxiliary data such as flat fields being linked to from `INFO_URL`. The harvesting will have to be restricted somehow - presumably limited to links pointing beside or below `INFO_URL`[^footnote-8] and `OBS_LOG`.

[^footnote-8]: E.g., with `INFO_URL``='http://some.site/this/guide.html'`,documents `http://some.site/this/manual.pdf` and `http://some.site/this/subdirectory/auxiliary.dat` might be harvested if it is (recursively) referenced from `guide.html`, but not `http://some.site/other/use.pdf`.

Any other administrative information pertaining to the file should also be included at the `INFO_URL`.

Proprietary data should be marked by setting the keyword `RELEASE` to the date at which the data can be freely distributed. The keyword `RELEASEC` may be used to give contact information for one or more people (name/email addresses, comma separated) administering the release details.

(10.0)=
# 10 Reporting of events detected by the pipeline/spacecraft

If the pipeline uses event/feature detection algorithms that will only work on the raw data, not the final pipeline product, detected events/features should be reported in pixel lists (see [Appendix I-d](#appendix-id)). If possible, events that are detected during acquisition of the data but are not detectable in the acquired data should also be reported (e.g., on-board-detected events in spacecraft).

When possible, such events/features should also be reported to relevant registries following the appropriate standards (e.g., VOEvents).
