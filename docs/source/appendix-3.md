(appendix-iii)=
# Appendix III. Meta-HDU mechanism

Most users expect to be able to analyse at least one file at a time on a laptop, preferably with all of the data loaded into memory. Thus, at some point, files become too large for comfort when following the guidelines for what to store in a single file/single Obs-HDU in a strict sense.

An obvious solution to this problem for a file that contains multiple Obs-HDUs would be to split it into multiple files containing only a single HDU each. However, at some point this strategy will not be enough to keep file sizes reasonable. E.g., simulation data are typically split into separate files for each time step and each variable. Thus, the issue of prohibitively large files should be dealt with in a more generic way while preserving the spirit of the guidelines for what should be stored together.

We do this by providing a mechanism that allows big HDUs to be split along one dimension into smaller Constituent HDUs stored in separate files and potentially individually recorded in an SVO as separately retrievable observation units, whilst also recording metadata for the original/unsplit HDU in a Meta-HDU without duplicating the data (having `NAXIS``=0`) and showing the relationship between the Constituent HDUs.

The Meta-HDU mechanism makes it easier to follow the guidelines for what to store together in a single Obs-HDU, by interpreting them as guidelines for what to store together in a single “Meta-Obs-HDU”.

All Constituent HDUs must have the same `EXTNAME`, and this will be the `EXTNAME` of the HDU that results if the Constituent HDUs are stitched together.

All Constituent HDUs must have `METADIM` set to the dimension that has been split. E.g., when splitting an array `[x,y,t]` into time chunks, `METADIM``=3`. Note that an accompanying auxiliary HDU with e.g., dimensions `[t,z]` would set `METADIM``=1`. Auxiliary HDUs whose data array dimensions does not contain the split dimension (e.g., flatfields) do not need to contain the `METADIM` keyword. It is allowed to have `METADIM > NAXIS` to account for lost trailing singular dimensions. E.g., if constituent HDUs have dimensions `[x,y,lambda]` and `METADIM``=5`, the resulting stitched HDU will have five dimensions e.g., `[x,y,lambda,1,t]`.

When possible, Constituent HDUs should contain all keywords describing the data, though some will have different values, e.g., `DATE-BEG`, `DATE-END` and keywords that vary as a function of the split dimension, or as a function of the data itself (e.g., `DATAMAX` and `DATAMIN`).

`CRPIXj` values in Constituent HDUs must refer to the same pixel in the original/unsplit HDU in order to keep all other WCS keywords identical among all Constituent HDUs. This implies that any `DATEREF` keyword should have the same value as well.

Extensions containing tabulated coordinates may also use the Meta-HDU mechanism, but they should then have `SOLARNET``=-1` (as all HDUs utilizing any of the mechanisms described in this document should have).

Pixel lists should use indices that apply to the referring Constituent HDUs (and must therefore be recalculated when the Constituent HDUs are stitched together).

The original/unsplit HDU is represented by a Meta-HDU containing a comma-separated list of files containing all Constituent HDUs (`METAFILS`), and `METADIM` set to _minus_ the value in the Constituent HDUs. Also, it should contain _header keywords representing the observation’s global attributes_ like duration, data statistics, cadence etc. A Meta-HDU may contain keywords that are not present in the constituent HDUs.

The Meta-HDU must have a set of WCS keywords that correctly describe the coordinates of the resulting stitched data array, including any added dimensions (any number of WCS coordinates may be specified irrespective of the number of dimensions in an HDU). The `WCSAXES` keyword must be set to the number of coordinates described by the set of WCS keywords.

The `EXTNAME` of such a Meta-Obs-HDU _must_ be the same as the `EXTNAME` of the constituent HDUs _with the string `';METAHDU'` appended_ (e.g., `'He I;METAHDU'`)

Using the keywords given above, it is now possible to reconstruct/stitch together Constituent HDUs from the files given in `METAFILS` into an ideal HDU with a correct header. It is also possible to reconstruct accompanying HDUs containing their corresponding variable keyword specifications and pixel lists (though care must be taken to adjust pixel indices!).

Although we recommend having a copy of the Meta-HDUs in each constituent file, this is not a requirement. In fact, for some pipelines, it makes sense to have Meta-HDUs only in the last file, since many of the global attributes are not known until the last constituent HDUs have been processed. When necessary, the Meta-HDU may even be in a separate file.

The Meta-HDU mechanism is not restricted to Obs-HDUs, it may be applied also by any HDU with `SOLARNET``=-1`.

(appendix-iiia)=
## Appendix III-a. Extension to multiple split dimensions

The mechanism above may be extended to splitting HDUs along multiple dimensions. In this case, the keywords `METADIMn` should be used to indicate which dimensions have been split. It is then possible to construct Meta-HDUs resulting from aggregating Constituent HDUs along one or more dimensions. I.e., if an original HDU with dimensions `[1000, 2000, 3000]` has been split into 100 files/HDUs with dimensions `[100,2000,300]`, the Constituent HDUs would have `METADIM1=1` and `METADIM2=3`.

Now it is possible to construct one set of Partial Meta-HDUs with `METADIM1=1` and `METADIM2=-3` representing the result of stitching together Constituent HDUs along dimension 3, i.e., representing a set of HDUs with dimensions `[100,2000,3000]`.

It is also possible to construct another set of Partial Meta-HDUs with `METADIM1=-1` and `METADIM2=3` representing the result of stitching together Constituent HDUs along dimension 1, i.e., representing a set of HDUs with dimensions `[1000,2000,300]`.

Finally, there should be a Meta-HDU with `METADIM1=-1` and `METADIM2=-3` representing the result of stitching together all Constituent HDUs, i.e., representing the original HDU with dimensions `[1000,2000,3000]`. This final, top-level Meta-HDU should have an `EXTNAME` ending with `“;METAHDU;METAHDU”`, whereas the `EXTNAMEs` of Partial Meta-HDUs should have only one `“;METAHDU”` attached. For even higher numbers of split dimensions, the rule is to add one copy of `“;METAHDU”` per layer when going from Constituent HDU towards the top level Meta-HDU.
