(12.0)=
# 12 Mandatory keyword for all HDUs (Section 2.1)

In addition to all keywords required by the FITS Standard, all HDUs (including the primary HDU) in SOLARNET FITS files must contain the keyword `EXTNAME`, with a value that is unique within the file.

```none
EXTNAME= 'He_I ' / Name of HDU
```

(13.0)=
# 13 Mandatory keywords for all Obs-HDUs (Section 2.2)

```none
SOLARNET= 0.5 / Fully SOLARNET-compliant=1.0, partially=0.5
OBS_HDU = 1 / This HDU contains observational data
DATE-BEG= '2020-12-24T17:12:00.5' / Date of start of observation
```

(14.0)=
# 14 Mandatory WCS keyword for all HDUs with a UTC (time) coordinate (Section 4.1)

```none
DATEREF = '2020-12-24T00:00:00' / Time coordinate zero point
```

(15.0)=
# 15 Mandatory keywords for fully SOLARNET-compliant Obs-HDUs

The keywords listed in this section are mandatory for fully SOLARNET-compliant Obs-HDUs. However, most keywords are only “conditionally mandatory”, depending on the data content, which mechanisms have been used, instrument type, etc.

(15.1)=
## 15.1 Mandatory general keywords (Sections 8, 9, and [Appendix V-a](#appendix-va))

```none
FILENAME= 'sleep_a_zen_l2_20201224_170000.1_balanced.fits'
DATASUM = '250353142' / Data checksum
CHECKSUM= 'hcHjjc9ghcEgh9g' / HDU checksum
DATE = '2020-12-31T23:59:59' / Date of FITS file creation
ORIGIN = 'University of Oslo' / Location where FITS file has been created
```

(15.2)=
## 15.2 Fundamental WCS coordinate keywords (Section 3.1)

Obs-HDUs must contain all WCS coordinate specifications that are required to _adequately describe the observations_ for their normal use. This includes e.g., the use of extra coordinates for singular dimensions when necessary (i.e., `WCSAXES` may be greater than `NAXIS`), or the use of alternate WCS coordinate systems (with WCS keywords ending in a letter `A-Z`). Normally, WCS keywords that must be included are `CRVALi`, `CDELTi`, `CRPIXj`, `CUNITi`, `CTYPEi`, and when necessary, also e.g., `WCSAXES`, `PCi_j` (or `CDi_j`), `CRDERi`, and `CSYERi`.

The example below is a brief excerpt of a header describing an observation where the random and systematic errors in the time coordinate are so large that they may be important for certain types of analysis.

```none
CTYPE3 = 'UTC ' / Coordinate 3 is time
CUNIT3 = 's ' / Units for time coordinate
CRPIX3 = 1 / Reference pixel: time starts at first image
CRVAL3 = 0 / [s] Offset from DATEREF of reference pixel
CDELT3 = 0.1 / [s] Sampling is 0.1 seconds
CRDER3 = 0.03 / [s] Large random clock error (sample-to-sample)
CSYER3 = 5 / [s] Large systematic error, clock may be off by 5s
```

(15.3)=
## 15.3 Mandatory WCS positional keywords (Section 3.2)

(15.3.1)=
## 15.3.1 Mandatory for ground-based observatories (Section 3.2)

```none
OBSGEO-X= 5327395.9638 / [m] Observer's fixed geographic X coordinate
OBSGEO-Y= -1719170.4876 / [m] Observer's fixed geographic Y coordinate
OBSGEO-Z= 3051490.766 / [m] Observer's fixed geographic Z coordinate
```

(15.3.2)=
## 15.3.2 Mandatory for Earth orbiting satellites (Section 3.2)

```none
GEOX_OBS= 1380295.0032 / [m] Observer's non-fixed geographic X coordinate
GEOY_OBS= 57345.1262 / [m] Observer's non-fixed geographic Y coordinate
GEOZ_OBS= 9887953.9454 / [m] Observer's non-fixed geographic Z coordinate
```

(15.3.3)=
## 15.3.3 Mandatory for deep space missions (not Earth orbiting satellites) (Section 3.2)

```none
HGLN_OBS= -0.0572950 / Observer's Stonyhurst heliographic longitude
HGLT_OBS= 5.09932 / Observer's Stonyhurst heliographic latitude
DSUN_OBS= 88981577950.3 / [m] Distance from instrument to Sun centre
```

(15.4)=
## 15.4 Mandatory data description keywords (Sections 5.1, 5.2 and 5.6.2)

The `BTYPE` keyword should contain either a UCD description of the data contents, or a more human readable description[^footnote-16]:

[^footnote-16]: For simulated data and simulated observations, `BTYPE` can be a plot axis description as in published Bifrost FITS files, with a further description given in `BNAME`, see Sections 5.1 and 15.1 of [S-META-SIM].

```none
BTYPE = 'phot.radiance;em.UV' / Unified Content Descriptors v1.23
```

_or_

```none
BTYPE = 'Spectral Radiance' / Type of data
```

Note that if a UCD description is given, a human readable description may instead be given by the optional keyword `BNAME`. On the other hand, if `BTYPE` gives a human readable description, the UCD description may instead be given by the optional keyword UCD. See Section 18.5 for examples.

```none
BUNIT = 'W/m2/sr/nm' / Physical units of calibrated data
XPOSURE = 2.44 / [s] Accumulated exposure time**
```

When the data are a result of multiple summed exposures with identical exposure times, the keyword `TEXPOSUR` and `NSUMEXP` must be set:

```none
TEXPOSUR= 1.22 / [s] Single-exposure time
NSUMEXP = 2 / Number of summed exposures
```

`NBINj` and `NBIN` is mandatory if the data has been binned:

```none
NBIN1 = 2 / Binning in dimension 1
NBIN2 = 4 / Binning in dimension 2
NBIN = 8 / Product of all NBINj
```

Missing or blank pixels in floating-point-valued HDUs should be set to _NaN_, but missing or blank pixels in integer-valued HDUs must be given the value of `BLANK`:

```none
BLANK = -100 / Value of missing pixels (integer HDU)
```

(15.5)=
## 15.5 Mandatory keywords identifying the origin of the observations (Section 6)

A _subset_ of the following keywords is mandatory in the sense that the subset must be sufficient to uniquely identify the origin of the observations, and they should be present to the extent that they make sense for the given observations (e.g., `MISSION` might not make sense for ground-based observations, or there might be no sensible value for `PROJECT`).

```none
PROJECT = 'Living With a Star' / Name of project
MISSION = 'SLEEP ' / Name of mission
OBSRVTRY= 'SLEEP A ' / Name of observatory
TELESCOP= 'ZUN ' / Name of telescope
TELCONFG= 'STANDARD' / Telescope configuration
INSTRUME= 'ZUN ' / Name of instrument
CAMERA = 'cam1 ' / Name of camera
GRATING = 'GRISM_1 ' / Name of grating/grism used
FILTER = 'Al_med, open' / Name of filter(s)
DETECTOR= 'ZUN_A_HIGHSPEED1' / Name of detector
OBS_MODE= 'lo-res-hi-speed12b' / Name of predefined settings used during obs.
SETTINGS= 'fpos=123,vpos=3' / Additional instrument/acquisition settings
OBSTITLE= 'High cadence active region raster'/ Title of observation
OBS_DESC= 'High cadence raster on AR10033'/ Description of observation
OBSERVER= 'Charlotte Sitterly' / Who acquired the data
PLANNER = 'Natalia Stepanian' / Observation planner
REQUESTR= 'Annie Maunder' / Who requested this particular observation
AUTHOR = 'Cecilia Payne' / Who designed the observation
CAMPAIGN= 'FlareHunt791,JOP922'/ Coordinated campaign name(s)
CCURRENT= 'sleep_a_zen_l2_20201224_170000_120_balanced.fits,&' / Concurrent,
CONTINUE 'sleep_b_zen_l2_20201224_170001_045_balanced.fits,&' / overlapping
CONTINUE 'sleep_a_magneto_l2_20201224_170001_030_full.fits,&' / observations
CONTINUE 'sleep_b_magneto_l2_20201224_170001_808_full.fits,&' / (multiple files)
CONTINUE 'sleep_b_magneto_l2_20201224_170001_909_full.fits' /

DATATAGS= '"ESA", "NASA", "ESA/NASA"'/ Additional information
```

Note that e.g., `DETECTOR`, `GRATING`, and `FILTER` this might seem unnecessary for instruments with an _a priori_ single fixed value, but for ground-based observatories, upgrades of an instrument might include a change of e.g., filters.

(15.6)=
## 15.6 Mandatory keywords for spectrographs and filter instruments (Sections 3.2 and 5.4)

```none
WAVEUNIT= -10 / Wavelength related kwds have unit: 10^(WAVEUNIT) m
WAVEREF = 'vac ' / Wavelength related kwds in vacuum
WAVEMIN = 582.10 / [Angstrom] Min wavelength covered by filter
WAVEMAX = 586.62 / [Angstrom] Max wavelength covered by filter
```

For spectrographs, and narrow-band filter instruments (when radial velocity is of importance when interpreting the observations), the following keyword is mandatory:

```none
OBS_VR = 36.62 / [km/s] Observer's outward velocity w.r.t. Sun
```

Also, to signal that no wavelength correction has been applied (even if the observer moves with respect to the Sun with a velocity given by `OBS_VR`) the following WCS keywords are mandatory:

```none
SPECSYS = 'TOPOCENT' / Coordinate reference frame = observer
VELOSYS = 0.0 / [m s-1] No velocity correction applied to WAVE coord.
```

(15.7)=
## 15.7 Mandatory keyword for spectrographs (Section 5.4)

```none
SLIT_WID= 0.5 / [arcsec] Slit width
```

(15.8)=
## 15.8 Mandatory keywords for polarimetric data (Section 5.4.1)

```none
POLCCONV= '(+HPLT,-HPLN,+HPRZ)' / Reference system for Stokes vectors
POLCANGL= 45.5 / [deg] Counter-clockwise rotation around +HPRZ axis
```

(15.9)=
## 15.9 Mandatory keyword for grouping (Sections 7 and [Appendix V-b](#appendix-vb) )

```none
POINT_ID= '20201224_165812_200'/ Unique (re-)pointing ID
```

(16.0)=
# 16 Mandatory keyword for SOLARNET HDUs that contain keywords with a definition in conflict with the specifications in this document (Section 2.2)

If a SOLARNET HDU contains SOLARNET keywords with definitions that are in conflict with the definitions in this document, those keywords _must_ be listed as a comma-separated list in the keyword `SOLNETEX`, e.g.:

```none
SOLNETEX= 'PLANNER, ATMOS_R0' / Exception: kws with conflicting definitions
```

Note that _none_ of the keywords that are mandatory for a given HDU may have conflicting definitions [^footnote-17].

[^footnote-17]: If some existing utility requires a different definition of a mandatory keyword, we recommend that the value for the non-SOLARNET definition be given in a new keyword, and that the software be modified.

(17.0)=
# 17 Mandatory keywords for all HDUs that uses any of the variable-keyword, pixel list or meta-observation mechanism (Sections 2.1, 2.2, 2.3, [Appendix I](#appendix-i), [Appendix II](#appendix-ii), and [Appendix III](#appendix-iii))

Any HDU using one of these mechanisms must have `SOLARNET` set to a non-zero value, even non-Obs-HDUs (which should use a value of -1). In addition, `EXTNAME` must be set according to the guidelines in Section 2. Finally, the respective `VAR_KEYS`, `PIXLISTS` or `METADIM`/`METAFILS` must be set – see [Appendix I](#appendix-i), [Appendix I-d](#appendix-id) and [Appendix III](#appendix-iii) for details.

```none
SOLARNET = -1.0 / SOLARNET mechanisms may be used
EXTNAME = 'zunhousekeeping' / Name of HDU
VAR_KEYS= 'He_I_T3;TEMPS' / Variable keyword used by this Aux-HDU
PIXLISTS= 'He_I_T3;T_IDX' / Pixel list used by this Aux-HDU
METADIM = 4 / Split dimension of meta-observation
METAFILS= 'sleep_a_zun_l2_20201224_165812.2_balanced.fits, &'
CONTINUE 'sleep_a_zun_l2_20201224_165912.4_balanced.fits, &'
CONTINUE 'sleep_a_zun_l2_20201224_170012.6_balanced.fits, &'
CONTINUE 'sleep_a_zun_l2_20201224_170112.8_balanced.fits, &'
CONTINUE '' / All files in Meta-obs
```

(17.1)=
## 17.1 Mandatory keyword for binary table extension value columns that use pixel-to-pixel association ([Appendix I-b](#appendix-ib))

The value of `WCSNn` must start with `“PIXEL-TO-PIXEL”` to signal that a direct pixel-to-pixel association applies:

```none
WCSN5 = 'PIXEL-TO-PIXEL' / Column 5 uses pixel-to-pixel association
```

(17.2)=
## 17.2 Mandatory keywords for binary table extensions that use the SOLARNET pixel lists mechanism for flagging pixels ([Appendix I-d](#appendix-id))

Binary table columns storing pixel indices must have `TCTYPn` equal to `'PIXEL'` and `TTYPEn` equal to `'DIMENSIONk'`, where k is the dimension number in the referring HDU’s data cube. The column storing pixel types must have `TTYPEn` equal to `'PIXTYPE'`. Any attribute columns must have `TTYPEn` equal to the name of the attached attribute contained in that column. E.g.:

```none
TTYPE1 = 'DIMENSION1' / Col.1 is index into data cube dimension 1
TTYPE2 = 'DIMENSION2' / Col.2 is index into data cube dimension 2
TTYPE3 = 'DIMENSION3' / Col.3 is index into data cube dimension 3
TTYPE4 = 'PIXTYPE' / Col.4 is the pixel type
TTYPE5 = 'ORIGINAL' / Col.5 contains original values of listed pixels
TCTYP1 = 'PIXEL ' / Indicates that col. 1 is a pixel index
TCTYP2 = 'PIXEL ' / Indicates that col. 2 is a pixel index
TCTYP3 = 'PIXEL ' / Indicates that col. 3 is a pixel index
```

(18.0)=
# 18 Optional keywords for all Obs-HDUs

The keywords in this section are optional for both fully and partially SOLARNET-compliant Obs-HDUs.

(18.1)=
## 18.1 Optional keyword for deep space missions (not Earth orbiting satellites) (Section 3.2)

In addition to the mandatory keyword DSUN_OBS the optional keyword `DSUN_AU` may be used to give the instrument-Sun centre distance in astronomical units:

```none
DSUN_AU = 0.594805136980 / [AU] Distance from instrument to Sun centre
```

(18.2)=
## 18.2 Optional date and time keywords (Section 4)

```none
DATE-END= '2020-12-24T17:00:02.5' / Date of end of observation
DATE-AVG= '2020-12-24T17:00:01.3' / Average date of observation
TIMESYS = 'UTC ' / Time scale of the time-related keywords.
```

(18.3)=
## 18.3 Optional keywords describing cadence (Section 5.3)

```none
CADENCE = 2.5 / [s] Planned cadence
CADAVG = 2.45553 / [s] Average actual cadence
CADMIN = 2.27943 / [s] Minimum actual frame-to-frame spacing
CADMAX = 2.69162 / [s] Maximum actual frame-to-frame spacing
CADVAR = 0.0118546 / [s] Variance of frame-to-frame spacing
```

(18.4)=
## 18.4 Optional keyword for spectrographs (Section 5.4)

```none
WAVECOV = '70.351919-70.839504, 76.749034-77.236619, 77.743708-78.231293, 78.3&' 
CONTINUE '67817-78.991925, 97.496379-97.842807, 102.2309-102.82752, 102.99111&' 
CONTINUE '-103.31829, 103.4049-104.00153&' / [nm] All WAVEMIN-WAVEMAX
```

(18.5)=
## 18.5 Optional data description keywords (Section 5.1)

```none
BNAME = 'Spectral Radiance' / Description of what the data array represents
UCD = 'phot.radiance;em.UV' / Unified Content Descriptors v1.23
```

(18.6)=
## 18.6 Optional keywords characterizing the instrument/data (Sections, 5.4 and 5.5)

```none
WAVEBAND= 'He I 584.58 A' / Strongest emission line in data
WAVELNTH= 584.61 / [Angstrom] Characteristic wavelength in vacuum
RESOLVPW= 6530 / Resolving power of spectrograph
FT_LOCK = 1 / Feature tracking on
ROT_COMP= 1 / Solar rotation compensation on (1)/off (0)
ROT_MODL= 'SNODGRASS' / Model used for rotation compensation
ROT_FORM= 'A+B*sin^2(phi)+C*sin^4(phi)' / Snodgrass & Ulrich 1990
AO_LOCK = 0.9 / Adaptive optics status, 0.0=no lock, 1.0=lock
AO_NMODE= 2 / Type of modes: Zernike, Karhunen-Loeve
```

For radio observations:

```none
BNDCTR = 198 / [GHz] Characteristic frequency in vacuum
```

The response function may be given in the variable keyword `RESPONSE`. If the data has been corrected for a variable response, the response function that has been applied should instead be given in `RESPAPPL`:

```none
RESPONSE= 0.76 / Mean of response function
```

_or_

```none
RESPAPPL= 0.52 / Mean of applied response function
```

(18.7)=
## 18.7 Optional quality aspects keywords (Sections 3.1 and 5.5)

```none
ATMOS_R0= 15 / [cm] Atmospheric coherence length
ELEV_ANG= 76.2 / [deg] Telescope elevation angle.
OBS_LOG = 'logs/2020/12/24/' / URL of observation log
RSUN_REF= 6.95508E+08 / [m] Solar rad. used for calc. px scale
COMPQUAL= 0.75 / Quality of data after lossy compression
COMP_ALG= 'jpeg2000' / Name of lossy compression algorithm
```

(18.8)=
## 18.8 Optional data statistics keywords (Section 5.6)

```none
DATAMIN = -23 / [DN] Minimum of data
DATAMAX = 4077 / [DN] Maximum of data
DATAMEAN= 144.794 / [DN] Mean of data
DATAMEDN= 11.0000 / [DN] Median of data
DATAP01 = -14 / [DN] 1st percentile of data
DATAP10 = -9 / [DN] 10th percentile of data
DATAP25 = -4 / [DN] 25th percentile of data
DATAP75 = 70 / [DN] 75th percentile of data
DATAP90 = 304 / [DN] 90th percentile of data
DATAP95 = 704 / [DN] 95th percentile of data
DATAP98 = 2085 / [DN] 98th percentile of data
DATAP99 = 2844 / [DN] 99th percentile of data
DATANP01= -0.099689 / DATAP01/DATAMEAN
...
DATANP99= 19.6417 / DATAP99/DATAMEAN
DATARMS = 471.524 / [DN] RMS dev: sqrt(sum((data-DATAMEAN)^2)/N)
DATANRMS= 3.25652 / DATARMS/DATAMEAN
DATAMAD = 3.43345 / [DN] Mean abs dev: sum(abs(data-DATAMEAN))/N
DATANMAD= 0.02371265 / DATAMAD/DATAMEAN
DATAKURT= 24.8832 / Kurtosis of data
DATASKEW= 4.84719 / Skewness of data
```

(18.9)=
## 18.9 Optional keywords for missing and saturated pixels (Section 5.6.1)

```none
NTOTPIX = 262144 / Expected number of data pixels
NLOSTPIX= 512 / Number of lost pix. b/c acquisition problems
NSATPIX = 4 / Number of saturated pixels
NSPIKPIX= 7 / Number of noise spike pixels
NMASKPIX= 71 / Number of masked pixels
NAPRXPIX= 64 / Number of approximated pixels
NDATAPIX= 261550 / Number of usable pix. excl lost/miss/spik/sat
PCT_LOST= 0.195312 / NLOSTPIX/NTOTPIX*100
PCT_SATP= 0.00152588 / NSATPIX/NTOTPIX*100
PCT_SPIK= 0.00267029 / NSPIKPIX/NTOTPIX*100
PCT_MASK= 0.02708435 / NMASKPIX/NTOTPIX*100
PCT_APRX= 0.02441406 / NAPRXPIX/NTOTPIX*100
PCT_DATA= 99.7734070 / NDATAPIX/NTOTPIX*100
```

(18.10)=
## 18.10 Optional pipeline processing keywords (Sections 8, 8.1 and 8.2)

```none
LEVEL = '3 ' / Data level of fits file
VERSION = 2 / FITS file processing generation/version
CREATOR = 'ZUN_MOMF_PIPELINE' / Name of software pipeline that produced the FITS file
VERS_SW = '2.5'       / Version of CREATOR software applied
HASH_SW = ' a7ef89ad998ea7feef4bbc0bbc1bbc2bbc3bbc4'/ GIT commit hash for pipeline
VERS_CAL= '2.4'       / Version of calibration pack applied
PRSTEP1 = 'MOMFBD ' / Processing step type
PRPROC1 = 'zun_momf.pro' / Name of procedure performing PRSTEP1
PRPVER1 = 1.5 / Version of procedure PRPROC1
PRMODE1 = 'BALANCED' / Processing mode of PRPROC1
PRPARA1 = 'ITER=5,MANUAL=1' / List of parameters/options for PRPROC1
PRREF1 = '<miss.influencer@esa.int>' / Factors influencing PRSTEP1
PRLOG1 = ' % Program caused arithmetic error: Integer divide by 0' / PRPROC1 log
PRENV3 = ' Kernel: Linux &'
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
CONTINUE 'dl_libs/astron/coyote' / Software library containing PRPROC1
PRVER1B = 59549 / Modified Julian date of last mirroring of PRLIB1B
```

(18.11)=
## 18.11 Optional keyword for administrative information (Section 9)

```none
INFO_URL= '<http://sleep.esa.int/zun/info.html>' / Data set resource web page
RELEASE = '2022-08-25T00:00' / Public release date of data
RELEASEC= '<embargo@zun.no>,<zunteam@esa.int>' / Data release administrators
```

(18.12)=
## 18.12 Optional keywords for grouping (Section 7)

```none
SVO_SEP1= 'POINT_ID,INSTRUME,DETECTOR,FILTER,NBIN' / Most fine grained separation
SVO_SEP2= 'POINT_ID,INSTRUME,DETECTOR,FILTER' / Img. shows target even w/binning
SVO_SEP3= 'POINT_ID,INSTRUME,DETECTOR' / Target identifiable in all filters
SVO_SEP4= 'POINT_ID,INSTRUME' / Still useful
SVO_GRP = 'R_SMALL_HRES_MCAD_Polar-Observations' / SVO group
MOSAICID= '10023b_2' / Mosaic ID
```

(18.13)=
## 18.13 Optional keyword for binary table extensions using the variable-keyword, pixel list or meta-observation mechanism ([Appendix I](#appendix-i), [Appendix I-d](#appendix-id) and [Appendix III](#appendix-iii))

`TDESCn` may be used to give a description of the contents of the binary table column.

```none
TDESC5 = 'Atmospheric coherence length values stored in this column are obtain&'
CONTINUE 'ned using the R0SUPER instrument, SW version 1.3'
```
