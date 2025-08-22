<style>
.new {
    background-color:rgb(252, 252, 147)
}
</style>
(appendix-vii)=
# <span class='new'>Appendix VII. External Extension References</span>

In SOLARNET FITS files, for keywords that have no special function within the official FITS/WCS framework, references to other extensions may be in the form of _external extension references_, e.g.:

```none
VAR_KEYS= '../auxiliary/s35837r001-aux.fits;VAR_KEY_DATA;TEMPERATURE[He_I]'
```

This means that the file with a relative path of `'../auxiliary/'` and a file name of `'s35837r001-aux.fits'` contains a binary table with `EXTNAME``='VAR_KEY_DATA'`, containing a column with `TTYPEn``='TEMPERATURE[He_I]'` which holds the data for the variable keyword `TEMPERATURE` (tagged with `[He_I]` to distinguish it from any other `TEMPERATURE`-containing columns). The path to the referenced file (`s35837r001-aux.fits`) is relative to the path of the referencing file.

In general terms, external extension references have the form `'<relative-path>/<filename>;<extname>'` and are drop-in replacements wherever plain extension names may be used. <span class=new>The relative path must always start with either './' or '../' and follow the conventions for "the traditional directory organisation for the applicable instrument/project". E.g., for a Solar Orbiter/SPICE Level 3 P file located in the directory `level3/2025/03/30`, the keyword</span>:

```none
DATAEXT='../../../../level2/2025/03/30/<L2 filename>;<extname>`
```

<span class=new>correctly reflects the SPICE directory structure `levelN/yyyy/mm/dd/<level N file>`.</span>

When looking up the file to locate the referenced extension, software should allow for any file name variations due to compression (e.g., endings like .gz and .zip). Also, if no file matches the relative path, an attempt should be made to locate the file in the same directory as the referencing file.

<span class='new'>As mentioned in [Appendix VIII](#appendix-viii) wildcards may be used also for directories, e.g., `PARENTXT``='../../../*/*/*/*9934.fits;MgIX'`, which would be useful in case e.g., data from a series of files spanning multiple days are concatenated into a single file, in a yyyy/mm/dd directory structure.</span>

## <span class='new'>Placeholder extensions</span>

Of course, the end user may not have the file containing the external extension available. To partially amend this situation, it is <span class=new>_strongly recommended to have a placeholder extension in the same file as the referring extension_, containing the full header of the referenced extension but no data cube, i.e., `NAXIS``=0` and no `NAXISn` keywords. Their original values should be given in `XNAXIS` and `XNAXISn`. `EXTNAME` is limited to 68 characters since the `CONTINUE` convention cannot be used for Fits Standard keywords, so external extension placeholder extensions shall be identified by having the keyword `EXT_EXT` set to the full value of the reference, including path, e.g., `EXT_EXT``='../auxiliary/s35837r001-aux.fits;VAR_KEY_DATA'`. When the reference includes wildcards, a "representative" placeholder can be given, with `EXT_EXT` still being identical to the reference, e.g., `EXT_EXT``='../../../*/*/*/*9934.fits;MgIX'` even though the placeholder stems from one particular file. The `EXTNAME` of an external extension placeholder is in principle arbitrary, though we recommend using the value of `EXTNAME` in the actual external extension whenever this is possible (it may not be, since `EXTNAME`s must be unique within a file).</span>
  
## <span class=new>Virtual external extensions</span>

<span class=new>It is also possible to have "virtual external extensions" which do not point to any actual file (it may not even ever have existed), solely for the purpose of providing a placeholder extension specifying its "theoretical" characteristics such as dimensionality and coordinate values using WCS keywords, `XNAXIS`, `XNAXISn` etc., or other kinds of metadata. For virtual external extensions, the path and filename should be simply `./`, such that the reference becomes `./;<extension name>`.</span>
