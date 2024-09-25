(appendix-iv)=
# Appendix IV. Adaptation to binary table extensions

This section outlines how to adapt the SOLARNET recommendations for data stored as columns in binary table extensions (Cotton et al.). It is written for an audience that already has experience in using binary table extensions for this purpose, so many details are deliberately left out.

For any column we consider the combination of column-specific keywords (`TTYPEn`, `TDIMn`, etc), general header keywords (`FILENAME`, `CREATOR`, etc), and the associated (column) data as a self-contained quasi-HDU, entirely analogous to the normal concept of an HDU. Thus, whenever the term HDU (as in Obs-HDU) is used elsewhere in this document, it may be taken to refer to such a quasi-HDU instead of an actual HDU.

However, for such quasi-HDUs, column-specific keywords replace general header keywords according to established standards and conventions for binary tables. E.g., for column `n`, `TDIMn` replaces `NAXIS` and `NAXISj`, `TZEROn` replaces `BZERO` etc. Almost all WCS keywords for image extensions have binary table column equivalents. For WCS keywords without a column-specific form, the value applies to all columns. Thus, if different values of such WCS keywords are necessary for separate columns, the data _must_ be placed in separate binary table extensions.

The column-specific keyword `TTYPEn` is normally used analogously to how `EXTNAME` is used for image extensions, but binary table extensions must also have an `EXTNAME` keyword set according to the rules in Section 2.

The column-specific keywords `TVARKn` replaces `VAR_KEYS`, and `TPXLSn` replaces `PIXLISTS` (see [Appendix I](#appendix-i) and [Appendix I-d](#appendix-id)).

The naming conventions for column-specific keywords (starting with `T` and allowing for 3-digit column numbers) leaves only 4 letters to carry meaning, which easily leads to the creation of very awkward column-specific keyword names. To alleviate this problem for keywords that must have different values for different columns, the column-specific keyword `TKEYSn` is introduced, listing pairs of keyword names and values inside a string. The [CONTINUE Long String Keyword Convention](https://fits.gsfc.nasa.gov/registry/continue_keyword.html) may of course be used to improve readability and add comments, e.g.:

```none
TKEYS3 = 'OBS_HDU=1, &' / Contains observational data  
CONTINUE 'DETECTOR=”ZUN_A_HIGHSPEED2”, &' / Detector 2  
CONTINUE 'WAVELNTH=1280 ' / [Angstrom] Principal wavelength
```

The syntax is relatively straightforward – a comma-separated list of keyword-value pairs, with string values in _double_ quotes. Spaces are ignored (except inside strings).

**Warning**: non-SOLARNET-aware FITS reading software will _not_ recognize values inside `TKEYSn`. Thus, FITS standard keywords – including WCS keywords – must never be given in `TKEYSn`. If no appropriate column-specific variant is valid and different values are necessary for different columns, the columns _must_ instead be stored in separate binary table extensions. Thus, `TKEYSn` should be used only for project-specific and SOLARNET-specific keywords.