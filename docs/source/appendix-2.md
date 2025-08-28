(appendix-ii)=
# Appendix II. Pixel list mechanism for flagging pixels

In some cases, it is useful to flag individual pixels or ranges of pixels within an Obs-HDU, or to store attributes (numbers or strings) that apply only to specific pixels or ranges of pixels (see Section 5.6.2). One example is to store the location of hot/cold pixels. Another example is to store the location and original values of pixels affected by cosmic rays/spikes. Yet another example might be to highlight or label (even with a string) specific points within the data cube – such as where a reduction algorithm has broken down.

Since the pixel list mechanism described here may be used by any HDU with a non-zero `SOLARNET` keyword, we will from now on simply use the term “referring HDU” for the HDU that uses this mechanism.

This mechanism uses a specific implementation of the pixel list FITS standard (Paper I, Section 3.2), where binary table extensions are used to store pixel indices and any attributes associated with each pixel.

The binary table extension must have `N + 1 + m` *columns* (or only `N + m`, see special case below), where `N` is the number of data cube dimensions in the referring HDU and `m` is the number of pixel attributes (may be zero). The `N` first *columns* contain pixel indices with `TTYPEn``='DIMENSIONk'`, where k is the dimension number in the referring HDU. Column number `N+1` must have `TTYPEn``='PIXTYPE'`. Any remaining columns must have `TTYPEn` set to the name of the attached attribute contained in that column, if any. Note that each cell of the binary table may only contain a single number or a string.

A zero-valued pixel index is a _wildcard_ representing all allowed pixel indices in the corresponding dimension.

The `PIXTYPE` column is used to classify each of these pixels into the categories described in _Table 1_ below.

| `PIXTYPE` | Meaning |
| --- | --- |
| 0   | Individual pixel |
| 1   | “Lower left” pixel (closest to (1, 1, …)) of a line/area/(hyper-)volume |
| 2   | “Upper right” pixel (farthest from (1, 1, …)) of a line/area/(hyper-)volume |

_Table 1: The meaning of values in the_ `PIXTYPE` _column. To flag individual pixels, one table row is needed to specify the pixel indices of each flagged pixel. For each pixel range to be flagged, two rows are needed: one specifying the “lower left” pixel indices and the other specifying the “upper right” pixel indices._

As a special case, the `PIXTYPE` column may be omitted if only single pixels are flagged. I.e., if no `PIXTYPE` column is present in a pixel list, all rows should be considered to be of type 0.

To establish the connection between the referring HDU and a pixel list, the referring HDU must contain the keyword `PIXLISTS`. `PIXLISTS` must declare the `EXTNAME` of the extension containing the pixel list, followed by a semicolon, then a comma-separated list of any pixel attribute names. When multiple pixel lists are used, this is signalled by adding a comma, the `EXTNAME` of the next pixel list extension followed by a semicolon, etc. Note that even when a pixel list does not contain any attributes, a comma is needed before the `EXTNAME` of any subsequent pixel list.

The `EXTNAME` of pixel lists may carry a meaning within the SOLARNET framework (e.g., `LOSTPIXLIST`, see Section 5.6.2). But if a pixel list `EXTNAME` ends with a “tag” (see [Appendix I](#appendix-i)), this does not change its meaning. Thus, such tags may be used to distinguish between different extensions containing pixel lists of the same type/meaning for different referring HDUs. Multiple referring HDUs may refer to the same pixel list, even if it has a tag.

As an example, in order to refer to all types of pixel lists mentioned in Section 5.6.2, the _referring HDU_'s `PIXLISTS` could contain the following:

```none
PIXLISTS= 'LOSTPIXLIST;, MASKPIXLIST;, &' / Lost and masked pixels
CONTINUE 'SATPIXLIST [He_I];ORIGINAL, &' / He_I saturated pixels w/original values
CONTINUE 'SPIKEPIXLIST [He_I];ORIGINAL,CONFIDENCE, &' / Spike pixels for He_I
CONTINUE 'SUNSPOTS;CLASSIFICATION' / Sunspot locations and classification
```

The pixel list name `SUNSPOTS` used above is arbitrarily chosen as an example, i.e., this `EXTNAME` does not carry any predefined meaning in a SOLARNET context.

**_Example 1 – Pixel list with attribute columns_**

The header of an Obs-HDU with dimensions `[lambda,x,y] = [20,100,100]` might contain the following entry:

```none
PIXLISTS= 'SPIKEPIXLIST;ORIGINAL,CONFIDENCE' / List of spike pixels
```

This means that `SPIKEPIXLIST` is a pixel list with two attribute columns, `ORIGINAL` and `CONFIDENCE`. The header of this binary table extension might include the following entries:

```none
EXTNAME = 'SPIKEPIXLIST' / Extension name
TTYPE1 = 'DIMENSION1' / Col.1 is index into data cube dimension 1
TTYPE2 = 'DIMENSION2' / Col.2 is index into data cube dimension 2
TTYPE3 = 'DIMENSION3' / Col.3 is index into data cube dimension 3
TTYPE4 = 'PIXTYPE' / Col.4 is the pixel type
TTYPE5 = 'ORIGINAL' / Col.5 contains original values of listed pixels
TTYPE6 = 'CONFIDENCE' / Col.6 contains confidence values of spike detection
TCTYP1 = 'PIXEL ' / Indicates that col. 1 is a pixel index
TCTYP2 = 'PIXEL ' / Indicates that col. 2 is a pixel index
TCTYP3 = 'PIXEL ' / Indicates that col. 3 is a pixel index
TPC1_1 = 1 / Indicates that col. 1 is a pixel index
TPC2_2 = 1 / Indicates that col. 2 is a pixel index
TPC3_3 = 1 / Indicates that col. 3 is a pixel index
```

Here, the presence of both `TCTYPn``='PIXEL'` and `TPCn_na``=1` for `n` between `1` and `3` signals that this binary table extension is a pixel list, and that columns `1` to `3` are pixel indices (see Paper I, Section 3.2). Conversely, since `TCTYPn` is not equal to `'PIXEL'` for columns `4`, `5` and `6`, these columns do not contain pixel indices. The use of `'PIXEL'` as a coordinate name (`TCTYPn`) is taken from Wells et al. (1981), Appendix A, Section III-F.

Thus, if we want to flag 3 pixels in the referring HDU data cube, and store the values `ORIGINAL` and `CONFIDENCE` for each pixel, the pixel list might contain the following table values (column headings are `TTYPEn` values):

|     | `DIMENSION1`<br>`(lambda)` | `DIMENSION2`<br>`(x)` | `DIMENSION3`<br>`(y)` | `PIXTYPE` | `ORIGINAL` | `CONFIDENCE` |
| --- | --- | --- | --- | --- | --- | --- |
| Row 1 (pixel #1) | 5   | 10  | 1   | 0   | 500 | 0.91 |
| Row 2 (pixel #2) | 5   | 11  | 1   | 0   | 489 | 0.91 |
| Row 3 (pixel #3) | 8   | 55  | 73  | 0   | 1405 | 0.98 |

**_Example 2_** **_– Pixel list with no attribute columns_**

We could list pixels that were lost during acquisition but were later filled in with estimated values. In this case, there is no original value, thus there are no attributes to associate with the pixels. An Obs-HDU might then contain:

```none
PIXLISTS= 'LOSTPIXLIST[He_I];' / EXTNAME of Binary table specifying lost pixels
```

In the pixel list binary table with `EXTNAME``='LOSTPIXLIST[He_I]'`, only 4 columns would be present `(N=3, m=0)` and the table values might be:

|     | `DIMENSION1`<br>`(lambda)` | `DIMENSION2`<br>`(x)` | `DIMENSION3`<br>`(y)` | `PIXTYPE` |
| --- | --- | --- | --- | --- |
| Row 1 (pixel #1) | 1   | 10  | 3   | 0   |
| Row 2 (pixel #2) | 2   | 10  | 3   | 0   |
| Row 3 (pixel #3) | 3   | 10  | 3   | 0   |

**_Example 3 – Pixel list using wildcard indices_**

Assuming the data cube comes from an aggregation of exposures (scanning) in the x direction, we want to flag three hot pixels on the detector for _all_ exposures (i.e., for all x indices). This is easily done using the following table in an extension with `EXTNAME``='MASKPIXLIST'`:

|     | `DIMENSION1`<br>`(lambda)` | `DIMENSION2`<br>`(x)` | `DIMENSION3`<br>`(y)` | `PIXTYPE` |
| --- | --- | --- | --- | --- |
| Row 1 (pixel #1) | 3   | 0   | 5   | 0   |
| Row 2 (pixel #2) | 9   | 0   | 8   | 0   |
| Row 3 (pixel #3) | 50  | 0   | 90  | 0   |

**_Example 4 – Pixel list flagging of a 2-dimensional range within a 4-dimensional data cube_**

As a real-life example, consider a 4-dimensional Solar Orbiter/SPICE data cube with dimensions `[x,y,lambda,t] = [1,1024,1024,1]`. The data was compressed onboard the spacecraft as 64 separate `[lambda,y] = [32,1024]` JPEG images. A telemetry packet belonging to the third of these JPEG images was lost during downlink. As a result, the third decompressed JPEG image, i.e., the `(x,y,lambda,t) = (1,*,65:128,1)` pixel range of the data cube, has approximated values. There are no original values or other attributes to be stored.

In the binary table pixel list we flag this pixel range by defining the “lower left” and “upper right” pixel of the pixel range by setting the `PIXTYPE` value to 1 and 2 respectively (see _Table 1_):

|     | `DIMENSION1`<br>`(x)` | `DIMENSION2`<br>`(y)` | `DIMENSION3`<br>`(lambda)` | `DIMENSION4`<br>`(t)` | `PIXTYPE` |
| --- | --- | --- | --- | --- | --- |
| Row 1 | 1   | 0   | 65  | 1   | 1   |
| Row 2 | 1   | 0   | 128 | 1   | 2   |

As in Example 3, we use a zero value as a wildcard for dimension 2, representing the range 1:1024. The same effect could have been achieved using values 1 and 1024 in row 1 and two, but this might be less readable to a human who is not familiar with the data set.

The header of the pixel list binary table extension pixel list describing the approximated pixel range would contain the values listed below (among others):

```none
EXTNAME = 'APRXPIXLIST[Full LW 4:1 Focal Lossy]' / Extension name

    ------------------------------
    | Column 1 specific keywords |
    ------------------------------
TTYPE1 = 'DIMENSION1' / Pixel indices dimension 1
TCTYP1 = 'PIXEL ' / Indicates that column 1 contains pixel indices
TDESC1 = 'Lower Left/Upper Right pixel indices of 1 approximated Lambda-Y ima&'
CONTINUE 'ge plane ranges due to loss of compressed telemetry packets&' / Axis
CONTINUE '' / labels for column 1

    ------------------------------
    | Column 2 specific keywords |
    ------------------------------
TTYPE2 = 'DIMENSION2' / Pixel indices dimension 2
TCTYP2 = 'PIXEL ' / Indicates that column 2 contains pixel indices
TDESC2 = 'Lower Left/Upper Right pixel indices of 1 approximated Lambda-Y ima&'
CONTINUE 'ge plane ranges due to loss of compressed telemetry packets&' / Axis
CONTINUE '' / labels for column 2

    ------------------------------
    | Column 3 specific keywords |
    ------------------------------
TTYPE3 = 'DIMENSION3' / Pixel indices dimension 3
TCTYP3 = 'PIXEL ' / Indicates that column 3 contains pixel indices
TDESC3 = 'Lower Left/Upper Right pixel indices of 1 approximated Lambda-Y ima&'
CONTINUE 'ge plane ranges due to loss of compressed telemetry packets&' / Axis
CONTINUE '' / labels for column 3

    ------------------------------
    | Column 4 specific keywords |
    ------------------------------
TTYPE4 = 'DIMENSION4' / Pixel indices dimension 4
TCTYP4 = 'PIXEL ' / Indicates that column 4 contains pixel indices
TDESC4 = 'Lower Left/Upper Right pixel indices of 1 approximated Lambda-Y ima&'
CONTINUE 'ge plane ranges due to loss of compressed telemetry packets&' / Axis
CONTINUE '' / labels for column 4

    ------------------------------
    | Column 5 specific keywords |
    ------------------------------
TFORM5 = '1I ' / Integer*2 (short integer)
TTYPE5 = 'PIXTYPE ' / Pixel type
TDESC5 = 'Pixel index types: 1 = lower left corner indices, 2 = upper right&'
CONTINUE ' corner indices' / Axis labels for column 5
```