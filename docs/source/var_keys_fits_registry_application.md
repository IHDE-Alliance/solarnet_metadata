# Variable-keyword Convention for FITS

**Status:** Proposed for the Registry of FITS Conventions
**Document version:** 1.0
**Date:** 2026-10-31

## Registry description

The Variable-keyword Convention associates values stored in another FITS HDU with a keyword in a referring HDU. The `VAR_KEYS` header keyword identifies the value-bearing binary-table columns or image extensions, optionally distinguishes multiple columns for the same keyword referenced from different HDUs with tags, and supports lookup by shared WCS coordinates or by exact pixel-to-pixel correspondence. The same mechanism supports array-valued keywords that are independent of the referring HDU's coordinates or dimensions. The convention is used in the SOLARNET Metadata Recommendations for Solar Observations.

## Responsible parties

Developed as part of the SOLARNET Metadata Recommendations for Solar Observations by:

- Stein Vidar Hagfors Haugan, Institute of Theoretical Astrophysics, University of Oslo
- Terje Fredvik, Institute of Theoretical Astrophysics, University of Oslo

The SOLARNET Metadata Recommendations project is the originating organization. The contacts listed for the project are `prits-group@astro.uio.no`.

## History and use

The convention is documented in the SOLARNET Metadata Recommendations, version 1.4 (March 2021), and is described in more detail in the later versions of that document. Its exact first use in a FITS file has not been established; the approximate date of first use is no later than 2021, the earliest dated documentation presently identified.

The convention is documented as being used by CHROMIS FITS data available through the [Stockholm SST Archive](https://dubshen.astro.su.se/sst_archive/). A relevant description of the CHROMIS/CRISP processing pipeline is Löfdahl et al. (2021), [SSTRED: Data- and metadata-processing pipeline for CHROMIS and CRISP](https://ui.adsabs.harvard.edu/abs/2021A%26A...653A..68L/abstract). The SOLARNET documentation gives a CHROMIS example in which measured values depend on time and subfield size.

## 1. Purpose and scope

An observation may have associated measurements or metadata that vary across time, position, wavelength, or another coordinate or dimension. Examples include atmospheric conditions, detector temperatures, exposure times, and instrument response values. FITS has no general mechanism for associating these values to another HDU. This convention provides a link from a **referring HDU** to values stored in one or more other HDUs, and defines how those values are associated with the referring data. The association implicitly defines a variable keyword whose value is the set of values in the linked HDU(s) at the pixel or world coordinates of a point in the referring HDU. The convention supports both binary-table and image extensions for storing the values.

An extension of the convention also permits any keyword to be represented by an array even when its values have no coordinate association with the referring HDU. This may be used to represent e.g. an array of instrument settings, a list of packet identifiers, or a set of measurements that are not associated with any particular point in the referring data.

The convention adds no new FITS data encoding. It uses FITS header keywords, binary-table columns or image extensions, and (where used) FITS WCS coordinate descriptions. FITS files using it must otherwise conform to the FITS Standard and applicable WCS standards. In its original SOLARNET profile, a referring HDU uses the mechanism when its `SOLARNET` keyword has a non-zero value; as described here does not require other SOLARNET metadata.

A value may be numeric or string-valued. The convention does not prescribe units, physical meanings, or a method for calculating an optional representative scalar value in the referring header; these are defined by the data producer.

## 2. Terms

- **Referring HDU:** The HDU whose `VAR_KEYS` keyword declares one or more variable keywords.
- **Value HDU:** A binary-table or image extension containing the values declared by a referring HDU.
- **Value column:** A binary-table column containing the values for one declared variable keyword.
- **Tag:** Optional text appended in square brackets to a keyword name to distinguish separate value columns or image extensions that represent the same keyword for different referring HDUs.

## 3. Declaration with `VAR_KEYS`

A referring HDU shall contain a string-valued `VAR_KEYS` keyword. The value identifies each value HDU and the keyword values stored there. For binary-table storage, it also identifies the value columns.

For binary-table storage, the declaration consists of one or more groups of this form:

```text
EXTNAME;KEYWORD[,KEYWORD[tag]...]
```

A comma may be followed by another `EXTNAME;` group to identify a different binary-table extension. For example:

```text
VAR_KEYS = 'VAR-EXT-1;KEYWD_1,KEYWD_2[He_I_He_II],VAR-EXT-2;KEYWD_3'
```

This declares `KEYWD_1` and `KEYWD_2[He_I_He_II]` in the binary-table extension whose `EXTNAME` is `VAR-EXT-1`, and `KEYWD_3` in the extension whose `EXTNAME` is `VAR-EXT-2`.

Spaces in the `VAR_KEYS` value are ignored when interpreting the declaration. The `EXTNAME` shall identify the intended extension unambiguously within the file. The keyword name and optional tag together shall identify exactly one value column or image extension for that declaration.

A tag is optional. It is a string enclosed in square brackets immediately following the keyword name. The tag shall not contain a semicolon, comma, or square bracket. A tag has no intrinsic meaning to a reader; its purpose is only to distinguish values. Producers may choose tags freely. Deriving a tag from one or more referring HDU names can make files easier to interpret.

The `VAR_KEYS` value may use the FITS CONTINUE Long String Keyword Convention if it does not fit in one header card. The CONTINUE convention shall not be used for `TTYPEn` values: `TTYPEn` is defined by the FITS Standard and is not a long-string keyword under this convention.

## 4. Binary-table representation

For each declared keyword and optional tag, the value HDU shall be a binary-table extension. It shall contain exactly one value column whose `TTYPEn` string equals the declared keyword name followed immediately by the tag, if present. For example, `KEYWD_2[He_I_He_II]` in `VAR_KEYS` links to a column with `TTYPEn = 'KEYWD_2[He_I_He_II]'`.

Column number is not significant to the link. A reader locates the column by its `TTYPEn` value, not by its `TTYPEn` index. The column may contain scalar or array-valued elements. Its dimensions and, for coordinate association, its WCS metadata define the value array used for lookup.

The value HDU's `EXTNAME` shall match the name in the corresponding `VAR_KEYS` group. If multiple declared keywords share one value HDU, each has its own matching column.

## 5. Association by coordinates

Unless pixel-to-pixel association is explicitly selected (Section 6), a value column is associated with the referring HDU by shared WCS coordinates.

The WCS metadata for the value column describes the coordinates of its values. Coordinates are matched by coordinate type/name after applicable projection or coordinate transformations have been taken into account. Axis order and axis numbers need not be the same in the referring HDU and the value column. Their coordinate values, including any required reference values such as a time zero point, determine the correspondence. For example, `HPLN-TAN` and `HPLN-TAB` identify the same underlying `HPLN` coordinate for matching after their respective WCS transformations are applied.

For a point in the referring data, a reader shall:

1. Evaluate the referring HDU's WCS to obtain its world-coordinate values.
2. Select the coordinates shared with the value column, matching by coordinate type/name rather than axis number.
3. Apply the value column's WCS to locate the corresponding position in the value array.
4. Obtain the value or values at that position, using the interpolation required by the applicable FITS WCS rules where interpolation is needed.

Coordinate reference values that establish a common origin are part of the coordinate calculation. For example, where a time axis is expressed as UTC relative to `DATEREF`, both HDUs shall provide the required `DATEREF`, and the comparison shall use the absolute times obtained by combining each reference value with its coordinate value.

The value column need not include every coordinate present in the referring HDU. If its coordinates are a subset of the referring HDU's coordinates, the matching coordinates determine the value for a referring point. A value column may also contain coordinates or dimensions that are absent from the referring HDU. In that case, more than one value may apply to a point in the referring HDU; the resulting set of applicable values is the variable keyword's value for that point. Dimensions with no coordinate may likewise provide additional values.

If the value array has no coordinate in common with the referring HDU, it is treated as an unassociated array-valued keyword (Section 7).

## 6. Pixel-to-pixel association

Pixel-to-pixel association shall be used when values must be associated with data pixels by index rather than by floating-point WCS calculations. It is useful for discrete values, values measured in sync with observations, or other cases where interpolation between coordinate samples is not intended.

For a binary-table value column, pixel-to-pixel association is selected when the applicable `WCSNn` keyword for that column begins with the string `PIXEL-TO-PIXEL`. For an image value HDU, it is selected when the applicable `WCSNAMEa` keyword begins with `PIXEL-TO-PIXEL`.

When this mode is selected, WCS coordinates shall not be used to associate the value array with the referring HDU. The value array shall include every dimension of the referring data array, in the same order. A dimension for which the value is constant shall have length one in the value array. Additional dimensions may be appended after the referring dimensions to represent multiple values per referring pixel.

For each corresponding dimension, the value-array length shall be either the referring dimension length or an integral divisor of it. If the value-array length is the referring length divided by an integer factor `N`, the one-based index in the value array is

```text
p_value = floor((p_referring - 1) / N) + 1
```

A value-array length equal to the referring dimension length is the special case `N = 1`. Thus, for a referring cube of dimensions `(x, y, t)` and a value array of dimensions `(1, 1, 3)`, each successive value applies to an equal-sized consecutive group of time planes when the referring time dimension is divisible by three. Appended dimensions are indexed independently and return multiple values for each referring pixel.

The FITS axis and array-dimension ordering rules apply. For binary-table array columns, the array dimensions are described by `TDIMn` as specified by the FITS Standard.

## 7. Array-valued keywords without association

The mechanism may represent a set of values that does not vary as a function of any coordinate or dimension in the referring HDU. Declare the value HDU and keyword in `VAR_KEYS` as usual, and store the values in a value column or image array with no shared coordinates used for association. The value array may have any number of dimensions. For example, a one-dimensional array may record packet identifiers or a list of instrument measurements.

## 8. Image-extension representation

Image extensions may be used instead of binary tables. In this form, each entry in `VAR_KEYS` identifies one image extension by its `EXTNAME`; the extension name is the keyword name, followed by its optional tag. Each entry has the form `EXTNAME;`, and entries are comma-separated. The declaration ends with a semicolon. For example:

```text
VAR_KEYS = 'KEYWD_1;,KEYWD_2[He_I_He_II];'
```

This identifies image extensions named `KEYWD_1` and `KEYWD_2[He_I_He_II]`. The extension data provide the keyword values. Coordinate association and pixel-to-pixel association follow Sections 5 and 6, respectively, using the WCS metadata of the image extension.

## 9. Representative scalar values

A referring HDU may also contain a scalar header value for a variable keyword. This value is representative only; it does not replace or alter the values in the linked value HDU. Providing a representative value is recommended when useful, but is not mandatory. The producer shall choose a statistic appropriate to the meaning of the keyword. An average is often suitable, but other choices, such as a maximum or minimum, may be more appropriate. String-valued variable keywords are permitted.

## 10. Limits and producer responsibilities

This convention defines the links and association modes but does not prescribe physical units, value validity criteria, null-value policy, behavior when a coordinate query falls outside the value array's coverage, or the choice of a representative scalar. Data producers shall document such application-specific semantics where relevant. A reader shall not infer that a tag encodes a coordinate, unit, or other meaning.

## 11. FITS keyword dictionary text

**Short description:** `VAR_KEYS` declares variable keyword values stored in other HDUs of the same FITS file. It identifies the value extensions and, for binary tables, the columns by keyword name and optional tag. The values may be associated with the referring HDU by shared WCS coordinates, by pixel-to-pixel indexing, or may form an independent array.

**Keyword definition:**

- `VAR_KEYS` (string): A comma-separated declaration of the FITS extensions and variable keyword values associated with a referring HDU. In binary-table form, each group is `EXTNAME;KEYWORD[,KEYWORD[tag]...]`; each value is in the column whose `TTYPEn` matches the keyword name and optional tag. In image-extension form, each entry is `EXTNAME;`, where the extension name is the keyword name and optional tag. Shared WCS coordinates define association by coordinates; a `WCSNn` or `WCSNAMEa` value beginning with `PIXEL-TO-PIXEL` selects pixel-to-pixel association. A value with no shared coordinates may be an unassociated array.

**Convention-specific interpretation of existing WCS keywords:**

- `WCSNn` (binary-table column WCS name): When its value begins with `PIXEL-TO-PIXEL`, it selects pixel-to-pixel association for the corresponding value column; WCS coordinates are not used for that association.
- `WCSNAMEa` (image-extension alternate WCS name): When its value begins with `PIXEL-TO-PIXEL`, it selects pixel-to-pixel association for the image value array; WCS coordinates are not used for that association.

Other keywords used to describe the FITS HDUs, table columns, and coordinate systems retain the meanings defined by the FITS Standard and applicable WCS conventions, and the convention must not be applied to keywords already defined by those standards.

## 12. References

1. Haugan, S. V. H. and Fredvik, T. (2021), *SOLARNET Metadata Recommendations for Solar Observations*, version 1.4, [Zenodo record 5719255](https://doi.org/10.5281/zenodo.5719255). The current recommendations and later versions are available from the [SOLARNET Metadata project](https://solarnet-metadata.readthedocs.io/).
2. Pence, W. D. et al. (2010), “Definition of the Flexible Image Transport System (FITS),” *Astronomy & Astrophysics*, 524, A42. [FITS Standard](https://fits.gsfc.nasa.gov/fits_standard.html).
3. Cotton, W. D., Tody, D. and Pence, W. D. (1995), “Binary table extension to FITS,” *Astronomy and Astrophysics Supplement Series*, 113, 159–166. [ADS record](https://ui.adsabs.harvard.edu/abs/1995A%26AS..113..159C/abstract).
4. Greisen, E. W. and Calabretta, M. R. (2002), “Representations of world coordinates in FITS,” *Astronomy & Astrophysics*, 395, 1061–1077.
5. Löfdahl, M. G. et al. (2021), “SSTRED: Data- and metadata-processing pipeline for CHROMIS and CRISP,” *Astronomy & Astrophysics*, 653, A68. [ADS record](https://ui.adsabs.harvard.edu/abs/2021A%26A...653A..68L/abstract).
6. [Stockholm SST Archive](https://dubshen.astro.su.se/sst_archive/), public archive of Swedish 1-m Solar Telescope observations, including CHROMIS data.
