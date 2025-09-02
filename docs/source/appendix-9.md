<style>
.new {
    background-color:rgb(252, 252, 147)
}
</style>
(appendix-ix)=
# <span class='new'>Appendix IX. Higher-level (Level P) data: parameterized components</span>

One common type of higher-level data are results from analysing lower-level data by fitting of parameterized components (e.g., emission line profiles) to spectroscopic data by means of {math}`\chi^2` minimization, but so far there has been no standard mechanism for how to store such results in FITS files.

Below we describe a recommended scheme for storing such results, comprehensive enough to store any data resulting from fitting of additive and multiplicative parameterized components. The scheme allows for later manual inspection, verification, and (if desirable) modification of the results. We will refer to files using this scheme as “(SOLARNET) Level P”. We suggest that “P” is used as a suffix to the relevant data level number for such data. E.g., Solar Orbiter SPICE files using this scheme are referred to as SPICE Level 3P. _These files should be considered as a reference implementation of this recommendation_ and will be used as an example below. Below we use dimensions `[x,y,lambda,t]` simply as an example, since those are the dimensions used in SPICE Level 3P FITS files.

For a typical SPICE Level 2 data cube with dimensions `[x,y,lambda,t] = [400,400,32,100]`, fitting of a single Gaussian (with a specified rest wavelength) plus a zero-order polynomial is made for every `(x,y,t)` position. The final result is a data cube `[x,y,t,p] = [400,400,100,5]` where

- `(x,y,t,1)` is the fitted line peak intensity, {math}`I`
- `(x,y,t,2)` is the fitted line velocity {math}`v`
- `(x,y,t,3)` is the fitted line width {math}`w`
- `(x,y,t,4)` is the fitted constant background {math}`a` (in a zeroth-order polynomial)
- `(x,y,t,5)` is the *reduced* {math}`\chi^2` value from the fit

Thus, such SPICE Level 3P data are the best fitting parameters {math}`(I,v,w,a)` for the function:

```{math}
F(\lambda;I,v,w,a)=Gaussian(\lambda;I,v,w) + Polynomial(\lambda;a)
```
for each point `(x,y,t)`.

For readout windows with multiple significant emission lines, multiple Gaussians are used. When e.g., two Gaussians are used, the Level 3P data will be the best-fitting parameters {math}`(I_1,v_1,w_1,I_2,v_2, w_2, a)` of the function:

```{math}
F(\lambda;I_1,v_1,w_1,I_2,v_2, w_2, a)=Gaussian(\lambda;I_1,v_1,w_1) + Gaussian(\lambda;I_2,v_2,w_2) + Polynomial(\lambda;a)
```

for every point `(x,y,t)`, giving a Level 3P data cube with dimensions `[x,y,t,p] = [400,400,200,8]`, where (`x,y,t,1..3)`) is  {math}`(I_1,v_1,w_1)`, `(x,y,t,4..6)` is {math}`(I_2,v_2,w_2`), `(x,y,t,7)` is {math}`a`, and `(x,y,t,8)` is the reduced {math}`\chi^2` value from the fit.

Generally, for _n_ Gaussians and a constant background, the size of the parameter dimension would be 3n+1+1. For n Gaussians and a linear background, the size would be 3n+2+1 because the last component would be {math}`Polynomial(\lambda;a,b) = a + b\lambda`. Additional components may be defined, e.g., Voigt profiles,  instrument-specific components (broadened Gauss profiles for SOHO/CDS), or linked Gaussians (with a fixed {math}`\Delta\lambda`). Other components may be multiplicative, e.g., extinction functions.

Since the lambda coordinates for `(x,y,*,t)` are passed to the fitting function together with the corresponding data points, we refer to the lambda dimension as a “fitting dimension”, whereas dimensions `x`, `y`, and `t` are referred to as “result dimensions”. In principle, both the fitting dimensions and the result dimensions may be entirely different and in a completely different order for other types of data (e.g., a `STOKES` dimension may be included).

Since the lambda dimension does not appear in the resulting data cube, it is said to be “absorbed” by the fitting process.

In general, the scheme can be used to store data analysis results from fitting of any function on
the form:

```{math}
F(\lambda;\mathbf{p}) = \left( ((f_1(\lambda;\mathbf{p_1}) + f_2(\lambda;\mathbf{p_2}) + \cdots ) \cdot f_j(\lambda;\mathbf{p_j}) + \cdots \right) \cdot f_x(\lambda;\mathbf{p_x}) + \cdots
```

where {math}`f_n` are individual components, {math}`\mathbf{p_n}` are their parameters, and {math}`\mathbf{p}` is the aggregation of all parameters, by {math}`\chi^2` minimization of:

```{math}
\chi^2 = \sum_\lambda W(\lambda) \cdot (y(\lambda) - F(\lambda; \mathbf{p}))^2
```

where {math}`W(\lambda)` is the statistical weight of each pixel (typically {math}`1/\sigma^2` ) and {math}`y(\lambda)` is the original data. The bold font for {math}`\mathbf{p}` and {math}`\mathbf{p_n}` indicates vectors of/multiple parameters, distinguishing them from individual parameters in non-bold font.

To ensure that the result of the analysis can be interpreted correctly, the full definition of {math}`F(\lambda;\mathbf{p})` and its parameters must be specified in the header of the extension containing the result, using the following keywords:

**Mandatory general keywords for HDUs with SOLARNET Level P data**

`SOLARNET` must be set to either `0.5` or `1`, and `OBS_HDU``=2` _(not `1`!)_ signals that the HDU contains SOLARNET Level P data

<span class=new>In order to make the Level P format as broadly useful as possible by generic software in as many domains as possible, _HDUs containing Level P data (i.e., `OBS_HDU``=2`) are exempt from most SOLARNET metadata requirements_. Although it is recommended to propagate SOLARNET keywords from the parent extension(s) when available, it is also possible to attach the metadata through the `PARENTXT` keyword (see below). For HDUs with `OBS_HDU``=2`, parent extensions specified by `PARENTXT` are to be treated as if they are primary HDUs, with the `INHERIT` convention in use for the referring HDU.</span>

`ANA_NCMP` must be set to the number of components used in the analysis.

The `CTYPEi` of the parameter dimension must be `'PARAMETER'`, and the coordinate value must match the parameter number. Note that the Meta-HDU mechanism ([Appendix III](#appendix-iii)) may be used to split Level P data over multiple files along this dimension, so e.g., parameters from each component are stored in separate files. In such cases, all HDUs should contain a full complement of all keywords defined here (including those describing components whose parameters are not present in the file), and `CRPIXn` should be modified such that the `PARAMETER` coordinate is identical to what it would be if the data were stored in a single file.

**Mandatory keywords describing each component**

`CMP_NPn`: Number of parameters for component `n`

`CMPTYPn`: Component type, e.g.,
- `'Polynomial'`, a polynomial {math}`p_1 + p_2 \lambda + p_3 \lambda^2 + \dotsi` of order `CMP_NPn - 1`.
- `'Gaussian'`, a Gaussian {math}`p_1 e^{-1/2(\lambda - p_2)^2/p_3^2}`
- `'SSW comp_bgauss'`, a broadened Gaussian {math}`f(p_1, \dots, p_5)`, see SSW routine `comp_bgauss`
- `'SSW comp_voigt'`, a Voigt profile {math}`f(p_1, \dots, p_4)`, see SSW routine `comp_voigt`
- … etc. If you need additional component types, create an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues).

**Optional _functional_ keywords for each component**

`CMPMULn`: Indicates whether component n is multiplicative (`CMPMULn``=1`), in which case it is to be applied to the result of all previous components `n-1`, `n-2`, etc. This can be used for e.g., extinction functions. Default value is `0`.

`CMPINCn`: Indicates whether component `n` is included (`CMPINCn``=1`) or excluded (`CMPINCn``=0`) in the fit. This allows specification of components that would normally be included but for some reason (e.g., poor S/N ratio) has been left out for this particular data set. If `CMPINCn` is zero, additive components have a value of zero independent of the parameter values, and multiplicative components have a value of 1. Default value is 1, i.e., the component is included in the fit. The parameters in the data cube should be set to the initial values that would have been used if the component was included. If this is not feasible, the parameters should be set such that the component value would be zero if it had in fact been included.

**Optional _descriptive_ keywords for each component**

`CMPNAMn`: Name of component `n`, typically used to identify/label the emission line fitted, e.g., `'AutoGauss79.5'`, `'He I 584'`.

`CMPDESn`: Description of component `n`

`CMPSTRn`: Used by SSW’s `cfit` routines for the string to be included in composite function names. E.g., the function string for a Gaussian is `'g'`, and `'p1'` for a first-order polynomial. An automatically generated composite function of the two would be called `'cf_g_p1_'`.

Each component can have up to 26 parameters labelled with `a=A-Z`, corresponding to
component parameters {math}`p_a = p_1 \dots p_{26}`.

**Mandatory functional keyword for each parameter**

Below, `n` is the component number, and `a` is a letter (`A-Z`) specifying the parameter number within the component (e.g., `PUNIT1A` is the units for the first parameter of the first component, `PUNIT2B` is the units for the second parameter of the second component, etc.).

`PUNITna`: The units for parameter a of component `n`, specified according to the FITS Standard Section 4.3, e.g., `'nm'` or `'km/s'`.

**Optional functional keywords for each parameter**

`PINITna`: Initial value for {math}`p_a` used during fitting

`PMAXna`: Maximum value ({math}`p_a` has been clamped to be no larger than `PMAXna` during fitting)

`PMINna`: Minimum value ({math}`p_a` has been clamped to be no less than `PMINna` during fitting)

`PCONSna`: Set to 1 if {math}`p_a` has been kept constant during fitting

`PTRAna`: Linear transformation coefficient {math}`A` (default value 1), see below

`PTRBna`: Linear transformation constant {math}`B` (default value 0), see below

When `PCONSna``=1`, i.e., when {math}`p_a` has been kept constant during fitting, it does not mean that {math}`p_a` necessarily has the same value for all `(x,y,t)`. The parameter may have been set to different values at different points prior to the fitting and then not been allowed to change during subsequent fitting of the other parameters. I.e., for points where a parameter has been kept constant, the `PINITna` value does not apply. Using the example above, the data cube value for `(x,y,t,p)` can differ from `(x,y,t+1,p)` even if the corresponding `PCONSna` value is `1`. It is also possible to keep a parameter constant only at specific points `(x,y,t)` using a constant mask, see `CONSTEXT` below.

A Gaussian component is explicitly defined to be simply {math}`f(\lambda;p_1,p_2,p_3)=p_1 e^{-1/2(\lambda - p_2)^2/p_3^2}`. However, some may prefer to store results in modified form, such as velocities instead of line positions, and with varying definitions of line width (e.g., FWHM). To accommodate this without having to create separate components for every form, it is possible to use the `PTRAna` and `PTRBna` keywords to define a linear transformation between the _nominal_ (stored) value {math}`n_a`) of a parameter and the actual value {math}`p_a`) that is passed to the component function.

Given {math}`A_a`=`PTRAna` and {math}`B_a`=`PTRBna`, the actual parameter value passed to the component function is {math}`p_a = A_a \cdot n_a + B_a` and conversely {math}`n_a = \frac{p_a - B_a}{A_a}`. If we set {math}`A = \frac{\lambda_0}{c}` and {math}`B = \lambda_0` then:

```{math}
n_a = \frac{c(p_a - \lambda_0)}{\lambda_0}
```

Thus, if {math}`p_a = \lambda_c` (the fitted line centre) then the nominal value stored in the data cube is {math}`n_a = v` (the line velocity, with positive values for red shifted lines).

Likewise for the third parameter of a Gaussian, if {math}`A = \frac{1}{2\sqrt(2ln2)}` then the nominal value stored in the data cube will be the full width of half maximum (FWHM).

**Optional descriptive keywords for each parameter**

`PNAMEna`: Parameter name, e.g., `'intensity'`, `'velocity'`, `'width'`

`PDESCna`: Parameter description

**Optional functional keywords for the analysis as a whole**

During the fitting process, one or more data coordinates/dimensions may be absorbed/removed and will not appear in the result extension. In the example above, the {math}`\lambda` coordinate and the corresponding dimension is absorbed. The following keywords describe the absorbed/removed coordinates/dimensions. Note that `m` does not refer to the coordinate number, it is just a counter starting with 1 for the first absorbed/removed coordinate or dimension, 2 for the second, etc. In the example above, there is only one absorbed/removed coordinate and dimension, so only `m=1` is used. Note also that in FITS, *there is no automatic correspondence between coordinates and dimensions* (if the `PCi_j` matrix is not diagonal), so the keywords below refer to coordinates and dimensions separately. In theory, a coordinate may disappear while no dimension disappears, or vice versa.

`XTYPEm`: <span class=new>The `CTYPE` of the m<sup>th</sup> coordinate(s) that was absorbed/removed during the fitting process (typically `XTYPE1``='WAVE'` for a disappearing {math}`\lambda` coordinate).</span>

`XDIMENm`: <span class=new>The dimension number of the m<sup>th</sup> absorbed dimension, counting left to right starting with 1. For SPICE Level 3 P files `XDIMEN1``=3`.</span>

<span class=new>`SIGMADAT`: Specification of the standard deviation {math}`\sigma` of the data used in the fitting process, given as a formula, a curve, or a pixel-by-pixel specification, see [5.5 Quality aspects](#5.5). When used in a Level P extension, the occurrence of `data` in a formula refers to the data cube in the `DATAEXT`. Keywords used in the formula that are not specified in the Level P extension should be taken from the header of the `DATAEXT` (note that they may be variable keywords). If `SIGMADAT` is not present (in neither the Level P extension nor the `DATAEXT` extension), {math}`\sigma` is assumed to be constant across all pixels. The value of `SIGMADAT` in a Level P data extension takes precedence over any occurrence in the `DATAEXT` extension.</span>

<span class=new>`CHISQAVG`: Specification of the average *reduced* {math}`\chi^2` value of the fit. A higher than usual value would be a good indicator that something has gone systematically wrong (not just at single points). If the fitted model is correct and the error estimates (`SIGMADAT`) are correct, the average reduced {math}`\chi^2` should be close to 1.</span>

To allow manual inspection, verification, and modification of the analysis results, several auxiliary data arrays may be stored in separate HDUs, with their `EXTNAME` given in the following keywords. In the description we specify their dimensionalities that would result from the example discussed above.

`RESEXT`: The HDU containing the analysis results ([x,y,t,p]). Note OBS_HDU=2

`DATAEXT`: The original data/Obs-HDU (`[x,y,lambda,t]`). <span class=new>`DATAEXT` will often be an external extension (see [Appendix VII](#appendix-vii)). In this case, although not mandatory, it is _strongly recommended to include a placeholder extension_, as this allows e.g., reconstruction of all coordinates and dimensions of the original data. If necessary, it may be a minimal extension with little metadata other than to specify coordinates and data dimensions through `XNAXIS`, `XNAXISn` and the WCS keywords.</span>

`PARENTXT`: <span class=new>A reference (external or local) to the parent extension containing the original data. The value of this keyword will often be identical to `DATAEXT`, but not necessarily: the original data may have been modified prior to the analysis, e.g., by applying e.g., cosmic ray removal, flatfielding etc.</span>

`RESIDEXT`: Residuals from the fitting process (`[x,y,lambda,t]`) which may in some cases be an important factor in the verification e .g., to discover emission lines that have not been considered during the fitting. This extention is normally not included, since it can be calculated from the original data and the fit paramters.

`CONSTEXT`: Constant mask (`[x,y,t,p]`). If constant mask `(x,y,t,p)` is 1 (not zero), parameter `p` has been kept constant/frozen *at the present value* (not necessarily the initial value) during the fitting process for point `(x,y,t)`. When the constant mask extension is not present, it is assumed that all parameters have been fitted freely (between the specified min and max values) at all times unless `PCONSn``a=1 `. <span class=new>`CONSTEXT` may also be specified as a pixel list ([Appendix II](#appendix-ii)). If the list contains an entry `(x,y,t,p)`, it means that the value of `(x,y,t,p)` in the result cube has been kept constant.</span>

`INCLEXT`: Component inclusion mask (`[x,y,t,n]`). If `(x,y,t,n)=0`, component `n` has not been included for point `(x,y,t)`. If `(x,y,t,n)=1`, the component has been included in the fit. When the extension is not present, it is assumed that all components have been included at all times. <span class=new>As for `CONSTEXT`, `INCLEXT` may be defined through the pixel list mechanism ([Appendix II](#appendix-ii)); if the list contains `(x,y,t,n)` then component `n` has *not* been included for point `(x,y,t,*)`. Where a component is not included, its parameter values should be set to `NaN`.</span>

In all such extensions, all WCS keywords that apply must be present, given their dimensionalities, as must all Level P-related keywords (including e.g., the extension names and component/parameter descriptions etc., and `OBS_HDU``=2` as these are also “Level P data"). For the component inclusion mask extension (`INCLEXT`), the `CTYPEi` of the component dimension should be `'COMPONENT'`.

For these auxiliary extensions, it may be worth considering the “external extensions” mechanism, see [Appendix VII](#appendix-vii).

At the time of writing, the SPICE Level 3P pipeline is not yet set in stone, and no Level 3P data has been delivered to the Solar Orbiter archive, thus there is no lock-in of the definitions yet. Please inform us by creating an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues) if you implement this mechanism.

**Extension to other types of higher-level data**

The Level P storage scheme may also be used for results from other types of analyses that do not involve forward modelling of the data and subsequent {math}`\chi^2` minimisation, as a way to store interrelated parameters that have been determined from data in other ways, e.g. Mg II k line parameters, with `CMPNAMn``='Mg II k'`, and `PNAMEna` set to e.g., `'k2v'`, `'k2r'`, or `'k3'`. For such cases, other values for the `CMPTYPn` keywords must be found (add an [issue](https://github.com/IHDE-Alliance/solarnet_metadata/issues)), and the size of the `PARAMETER` dimension will be equal to the sum of the `CMP_NPn` keywords, not the sum plus 1 as is normally the case.
