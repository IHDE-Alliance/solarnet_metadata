<resource schema="sst_sstred" resdir=".">
  <meta name="creationDate">2025-07-11T12:08:12Z</meta>
  <!-- 
   * VO TAP client: https://vespa.obspm.fr/planetary/data/
     - Cog wheel top of list, "custom" http://stw-main.utenforuio.no:8080/tap, schema sst_crisp
     - NOTE: The TAP service is available without declaring any services below!

   * Make sure we can serve download URLs.
     - NOT SETTING access_url: links to local file (through EPN-TAP VO client and local search form),
       the following seems to work to restrict access when combined with embargo and owner columns:

          dachs admin adduser sst <password> "SST group"
          dachs admin adduser steinhh <password> "Stein Haugan"
          dachs admin adduser mats <password> "Mats Lofdahl"
          dachs admin addtogroup mats sst
          dachs admin addtogroup steinhh sst

   * Normal import (new files only b/c we have <import updating="True"> and <ignoreSources>)

      - dachs import q.rd

   * Reimport (use when files have been updated, e.g. new keywords added to FITS headers, or new files added to the data directory)
      - dachs drop q.rd
      - dachs import q.rd
      - dachs pub q.rd
      - dachs serve      <== not necessary if service is already running as a daemon

   * Range search on date_beg (DATE-BEG): see <service> below, use e.g. 2021-01-01 .. 2022-01-01
     or 2021-01-01T12:00:00 .. 2022-01-01T14:00:00

   * Web page title and other things (contact info, logo etc) should be set in /etc/gavo.rc, but during development
     it can also be set in ~/.gavorc for the user that runs the serving process ("dachs serve debug").

  -->

  <meta name="title">Observations of the Sun by CRISP, CRISP2, or CHROMIS on the SST</meta>
  <meta name="description">
    This is high-resolution spectro-polarimetric solar data obtained
    with the CRISP, CRISP2, and CHROMIS imaging spectropolarimeters on
    the Swedish 1-Meter Solar Telescope (SST). The data products are
    cubes with dimensions: spatial (about 1000x1000 pixels), spectral
    (about 10 pixels), stokes (1-4 pixels), and temporal (1-100s of
    pixels with a cadence of a few seconds).
  </meta>
  <meta name="subject">solar-physics</meta>
  <meta name="creator">Lofdahl, M.; Haugan, S.</meta>
  <meta name="instrument">CRISP</meta>
  <meta name="instrument">CRISP2</meta>
  <meta name="instrument">CHROMIS</meta>
  <meta name="facility">Swedish 1-Meter Solar Telescope</meta>

  <!-- other choices: http://docs.g-vo.org/DaCHS/ref.html#procs-license-cc0 -->
  <STREAM source="//procs#license-cc-by" what="CRISP/CRISP2/CHROMIS cubes"/>

  <meta name="source"><![CDATA[2003SPIE.4853..341S#2026A&A...705A..55S]]></meta>
  <meta name="contentLevel">Research</meta>
  <meta name="contentLevel">University</meta>
  <meta name="type">Archive</meta>
  <meta name="coverage.waveband">Optical</meta>
  <meta name="referenceURL">https://dubshen.astro.su.se/sst_archive</meta>
  <meta name="site.description">Observatorio del Roque de los Muchachos, La Palma, Canary Islands, Spain</meta>



  <!-- _longdoc: from homepage click "Observations of the Sun by..." (meta: title),
      see below "Resource Documentation". Also shown if you click from there 
      on "Information on resource 'Observations of the Sun by...' (meta: title)",
      see below "This is high-resolution ..." (meta: description)
      -->
  <meta name="_longdoc" format="rst">
    <![CDATA[
             ==========
             Details
             ==========
             
             The data avaialable here are observations from the
             Swedish 1-meter Solar telescope (SST), using the imaging
             spectro(polari)meters CRISP, CRISP2, and CHROMIS. The
             data products are science-ready data cubes in FITS
             files, produced by running the SSTRED data processing
             pieline.
             
             The FITS files are all 5-dimensional, where the
             dimensions are [spatial, spatial, spectral, Stokes,
             repeat], although depending on the observing program or
             processing details, any of the latter three dimensions
             can be of length unity.
             
             The WCS coordinates are tabulated (except for the Stokes
             coordinate).
             
             =============
             References
             =============
             
             * The SST is described by Scharmer et al. (2003SPIE.4853..341S).
             
             * The spectro(polari)meters are described by Scharmer et al.
               (2026A&A...705A..55S).
             
             * SSTRED is described by Löfdahl et al. (2021A&A...653A..68L).
             
    ]]>
  </meta>


  <!-- We need to convert the wavelength range into Joules! -->
  <!-- E = hc/lambda = 6.626e-34 * 2.99792458e8 / lambda -->
  <!-- 500nm = 3.972e-19 J -->
  <!-- 854nm = 2.326e-19 J -->
  <coverage>
    <!-- Newer DaCHS versions: <spectral>500 854[nm]</spectral> -->
    <spectral>2.326e-19 3.972e-19</spectral>
  </coverage>

  <!-- *********** DATA MODEL *********** -->

  <table id="epn_core" onDisk="True" adql="True">
    <publish sets="local"/>
    <index columns="time_min"/>
    <index columns="time_max"/>
    <index columns="date_beg"/>

    <!-- See http://docs.g-vo.org/DaCHS/ref.html#the-epntap2-table-2-0-mixin
         for a complete list of optional_columns -->
   <!-- Re: spatial_frame_type: https://www.ivoa.net/documents/EPNTAP/20220822/REC-EPNTAP-2.0.html#:~:text=In%20order%20to,not%20in%20c3 -->
    <mixin
       spatial_frame_type="celestial"
       optional_columns="access_url access_format access_estsize thumbnail_url file_name
        publisher processing_level_desc
        filter spatial_coordinate_description spatial_origin time_scale
        obs_mode detector_name instrument_type orientation measurement_unit"
    >//epntap2#table-2_0</mixin>

    <mixin>//epntap2#localfile-2_0</mixin>
    
    <!-- time_min exists, but we want to be able to search using time stamp strings,
         see service below -->
    <column name="date_beg" type="timestamp"
        ucd="time.start"
        tablehead="DATE-BEG"
        description="Observation start time (UTC)"/>

    <column name="pol_states" type="text"
        ucd="meta.code;phys.polarization"
        utype="obscore:Char.PolarizationAxis.stateList"
        tablehead="Pol. States"
        description="List of polarization states in the data set"
        verbLevel="15">
        <property name="std">1</property>
    </column>

    <column name="pol_xel" type="bigint"
            ucd="meta.number"
            utype="obscore:Char.PolarizationAxis.numBins"
            tablehead="|Pol|"
            description="Number of elements (typically pixels) along the
                    polarization axis."
            verbLevel="10">
            <property name="std">1</property>
            <values nullLiteral="-1"/>
    </column>

  </table>

  <!-- *********** DATA IMPORT *********** -->

  <data id="import" updating="True">
    <!-- The asterisk implies inclusion of subdirectories -->
    <sources pattern="data/*_im.fits" recurse="True">
        <!-- Previously imported files will be ignored-->
        <ignoreSources fromdb="select accref from \schema.epn_core"/>
    </sources>

    <!-- qnd="False": drop optimisations that might cut off long headers(?) -->
    <fitsProdGrammar hdusField="hdus" qnd="False">
      <rowfilter procDef="//products#define">
          <bind key="table">'\schema.epn_core'</bind>
          <bind key="embargo">
             parseTimestamp(@RELEASE)
          </bind>
          <bind key="owner">"sst"</bind>
      </rowfilter>
    </fitsProdGrammar>

    <make table="epn_core">
      <rowmaker idmaps="*">
        <!-- Refer to http://docs.g-vo.org/DaCHS/ref.html#epntap2-populate-2-0
             for more information on the parameters.
        -->
         <apply>
                <!-- 
                -->
            <code><![CDATA[
                # When appropriate, WAVEMIN/WAVEMAX keywords can be used to fill in spectral keywords:
                #
                if "WAVEMIN" in vars and "WAVEMAX" in vars and "WAVEUNIT" in vars:
                    @spectral_range_max = LIGHT_C/(@WAVEMIN*10**@WAVEUNIT) if @WAVEMIN > 0 else None
                    @spectral_range_min = LIGHT_C/(@WAVEMAX*10**@WAVEUNIT) if @WAVEMAX > 0 else None

                # but if that is not possible for some reason, the bounding box keywords CBBMIN/CBBMAX
                # might be used if present and nonzero:
                #
                elif "CBBMIN3" in vars and "CBBMAX3" in vars:
                    @spectral_range_max = LIGHT_C/(@CBBMIN3*10**9) if @CBBMIN3 > 0 else None
                    @spectral_range_min = LIGHT_C/(@CBBMAX3*10**9) if @CBBMAX3 > 0 else None
                else:
                    @spectral_range_max = None
                    @spectral_range_min = None

                # Calculate spectral sampling step min in Hz.
                # delta Hz = Hz(lambda) - Hz(lambda + delta lambda)
                # Minimum wavelength step -> maximum frequency step, and vice versa
                #
                if "CSPMIN3" in vars and "CSPMAX3" in vars:

                    @_lambda = (@CBBMIN3+@CBBMAX3)/2*10**9

                    @_lambda_plus_min_step = @_lambda + @CSPMIN3*10**9
                    @spectral_sampling_step_max = LIGHT_C/@_lambda - LIGHT_C/@_lambda_plus_min_step

                    @_lambda_plus_max_step = @_lambda + @CSPMAX3*10**9
                    @spectral_sampling_step_min = LIGHT_C/@_lambda - LIGHT_C/@_lambda_plus_max_step
                else:
                    @spectral_sampling_step_min = None
                    @spectral_sampling_step_max = None

                @spectral_resolution = @RESOLVPW if "RESOLVPW" in vars else None

                # WAVEBAND may be appropriate for some, but not for SST data:
                @filter = @FILTER1 if "FILTER1" in vars else None

                # Wide-band: imaging
                # Narrow-band: spectropolarimetry or spectrometry, depending on whether NAXIS4 > 1
                if "OBS_MODE" in vars:
                    @obs_mode = @OBS_MODE.lower()
                else:
                   if @NAXIS4 == 1 and @NAXIS3 == 1: # No Stokes, no tuning, i.e., imaging
                       @obs_mode = "imaging"
                   elif @NAXIS4 > 1 and @NAXIS3 == 1: # Stokes but no tuning, i.e., polarimetry
                       @obs_mode = "polarimetry"
                   elif @NAXIS4 == 1 and @NAXIS3 > 1: # Tuning but no Stokes, i.e., spectrometry
                       @obs_mode = "spectrometry"
                   elif @NAXIS4 > 1 and @NAXIS3 > 1: # Stokes and tuning, i.e., spectropolarimetry
                       @obs_mode = "spectropolarimetry"

                if @obs_mode == "imaging":
                    @dataproduct_type = "im" if @NAXIS5 == 1 else "mo"
                    @ucd = ";".join([ "obs.image", "phot.flux", "em.opt" ])
                elif @obs_mode == "polarimetry":
                    # STOKES can be considered "colors", so im/mo are appropriate
                    @dataproduct_type = "im" if @NAXIS5 == 1 else "mo"
                    @ucd = ";".join([ "obs.image", "phys.polarization.stokes", "em.opt" ])
                elif @obs_mode == "spectrometry":
                    @dataproduct_type = "sc"
                    @ucd = ";".join([ "obs.image", "phot.flux.density", "em.opt" ])
                elif @obs_mode == "spectropolarimetry":
                    @dataproduct_type = "cu"
                    @ucd = ";".join([ "obs.image", "phot.flux.density", "phys.polarization.stokes", "em.opt" ])

                if @NAXIS5 > 1:
                    @ucd += ";time.series"
            ]]></code>
        </apply>
        <apply procDef="//epntap2#populate-2_0" name="fillepn">
          <!-- Note: <bind> (not <map>) inside <apply> tags -->
          <bind key="instrument_host_name">@TELESCOP</bind>
          <bind key="instrument_name">@INSTRUME</bind>
          <!-- For SST, CDELT1/2 are 1 b/c the coordinates are tabulated to account for tracking, 
               so we use the bounding box keywords to calculate the resolution in degrees. -->
          <bind key="c1_resol_max">(@CBBMAX1-@CBBMIN1)/(@NAXIS1-1)/3600</bind>
          <bind key="c1_resol_min">(@CBBMAX1-@CBBMIN1)/(@NAXIS1-1)/3600</bind>
          <bind key="c2_resol_max">(@CBBMAX2-@CBBMIN2)/(@NAXIS2-1)/3600</bind>
          <bind key="c2_resol_min">(@CBBMAX2-@CBBMIN2)/(@NAXIS2-1)/3600</bind>
      
          <bind key="c1min">@CBBMIN1/3600</bind>
          <bind key="c1max">@CBBMAX1/3600</bind>
          <bind key="c2min">@CBBMIN2/3600</bind>
          <bind key="c2max">@CBBMAX2/3600</bind>
      
          <bind key="modification_date">@DATE</bind>

          <bind key="dataproduct_type">@dataproduct_type</bind> 
          <bind key="granule_gid">'sst/sstred'</bind>
          <bind key="granule_uid">\srcstem</bind>
          <bind key="measurement_type">@ucd</bind>
          <!-- "obs_id associates granules derived from the same data (e.g. various representations/processing levels)". 
               For CRISP, both wideband and narrowband data are processed together during MOMFBD and subsequent steps, 
               thus both types of data are derived from the same raw data and should have the same obs_id.
               The same applies (individually) to CRISP2 and CHROMIS data (nb and wb).
               -->
          <bind key="obs_id">@POINT_ID if "POINT_ID" in vars else @FILENAME</bind>
          <!-- SST data have been processed with MOMFBD, destretched, etc. so they are
               level 5 in EPN-TAP according to this reference: 
               https://www.ivoa.net/documents/EPNTAP/20211022/PR-EPNTAP-2.0-20211022.html#tth_sEc1.3:~:text=meta.modelled%22%20appended.-,processing_level%C2%A0%C2%A0,-The%20processing_level%20parameter 
          -->
          <bind key="processing_level">5</bind>
          <bind key="service_title">"\schema"</bind>
          <bind key="spectral_range_max">@spectral_range_max</bind>
          <bind key="spectral_range_min">@spectral_range_min</bind>
          <bind key="target_class">'star'</bind>
          <bind key="target_name">'Sun'</bind>
          <bind key="target_region">'atmosphere'</bind>
      
          <bind key="time_exp_max">@XPOSURE</bind>
          <bind key="time_exp_min">@XPOSURE</bind>
          
          <bind key="time_max">dateTimeToJdn(parseTimestamp(@DATE_END))</bind>
          <bind key="time_min">dateTimeToJdn(parseTimestamp(@DATE_BEG))</bind>
          <bind key="time_scale">'UTC'</bind>
          <bind key="time_refposition">'TOPOCENTER'</bind>
          <bind key="time_sampling_step_min">@CADMIN</bind>
          <bind key="time_sampling_step_max">@CADMAX</bind>
          <bind key="spectral_resolution_min">@spectral_resolution_min</bind>
          <bind key="spectral_resolution_max">@spectral_resolution_max</bind>
          <bind key="spectral_sampling_step_min">@spectral_sampling_step_min</bind>
          <bind key="spectral_sampling_step_max">@spectral_sampling_step_max</bind>
          <bind key="release_date">@RELEASE</bind>
        </apply>
        <apply procDef="//epntap2#populate-localfile-2_0"/>

        <map key="pol_states">"/I/Q/U/V/" if @obs_mode == "spectropolarimetry" else "/I/"</map>
        <map key="pol_xel">@NAXIS4</map>
        <map key="file_name">@FILENAME</map>
        <map key="date_beg">@DATE_BEG</map>
        <map key="access_format">"application/fits"</map>
        <!-- NOT setting access_url would give appropriate "local" download link -->
        <map key="access_url">"https://dubshen.astro.su.se/sst_archive/download/"+@FILENAME</map>
        <map key="thumbnail_url">"http://stw-main.utenforuio.no:8080/static/"+\srcstem+".png"</map>
        <map key="publisher">"Institute for Solar Physics, Stockholm University"</map>
        <map key="processing_level_desc"><![CDATA["See 2021A&A...653A..68L"]]></map>
        <map key="filter">@filter</map>
        <!-- https://www.ivoa.net/rdf/refposition/2019-03-15/refposition.html -->
        <map key="spatial_origin">"HELIOCENTER"</map> 
        <!-- https://www.ivoa.net/documents/EPNTAP/20220822/REC-EPNTAP-2.0.html#:~:text=In%20order%20to,not%20in%20c3). -->
        <map key="spatial_coordinate_description">"HPC"</map>
        <map key="time_scale">"UTC"</map>
        <map key="obs_mode">@obs_mode</map>
        <map key="detector_name">@INSTRUME</map>
        <map key="instrument_type">"imaging spectropolarimeter"</map>
        <map key="orientation">@CROTA if "CROTA" in vars else None</map>
        <map key="measurement_unit">@BUNIT</map>
      </rowmaker>
    </make>
  </data>
  
  <!-- *********** SERVICES *********** -->
  <!-- NOTE: the "EPN-TAP service" accessible from VO clients exists without 
       declaring any services below!! -->
  <!-- "static" allows access to /var/gavo/web/nv_static/ under http:/..../static/-->
  <service id="experimental" allowed="form,static">
    <meta name="title">Experimental SST/SSTRED Data Access</meta>
    <meta name="shortName">Experimental form</meta>
    <meta name="description">
      Simple service for accessing the SST/SSTRED data, Vizier-like date
      search on DATE-BEG.
    </meta>
    <meta name="_intro" format="rst">
       <![CDATA[
         For advanced queries on this catalogue use ADQL_
         possibly via TAP_
         
         .. _ADQL: /adql
         .. _TAP: /tap
       ]]>
    </meta>
     <property name="staticData">data/static</property>    
    <publish render="form" sets="local"/>
    <dbCore queriedTable="epn_core" sortKey="time_min">
        <condDesc buildFrom="date_beg"/>
    </dbCore>
    <outputTable>
        <outputField name="date_beg" tablehead="DATE-BEG"/>
        <outputField name="granule_uid" tablehead="Granule ID"/>
        <outputField name="access_url" displayHint="type=url" tablehead="Data Access">
            <formatter><![CDATA[
                    return T.a(href=data, target="_blank")["Download"]
                ]]>
            </formatter>
        </outputField>
        <outputField name="thumbnail_url" type="text" ucd="meta.ref.url" tablehead="Thumbnail">
            <formatter><![CDATA[
                return T.img(src=data, alt="Error", style="max-width: 200px;")
            ]]></formatter>
        </outputField>
    </outputTable>
  </service>


  <!-- *********** REGRESSION TESTS *********** -->
  <!-- Optional: Regression tests to verify the service is working correctly -->
  <regSuite title="sst_sstred regression">
    <regTest title="SST/SSTRED EPN-TAP serves data">
      <url parSet="TAP" QUERY="SELECT TOP 1 * from sst_sstred.epn_core"
     >/tap/sync</url>
      <code>
        rec = self.getFirstVOTableRow()
        self.assertIsNotNone(rec.get("granule_uid"))
        self.assertIsNotNone(rec.get("time_min"))
        self.assertEqual(rec.get("target_name"), "Sun")
      </code>
    </regTest>
    
    <regTest title="SST/SSTRED web form returns results">
      <url parSet="form">/sst_sstred/web/form</url>
      <code>
        self.assertHasStrings("SST/SSTRED", "Solar")
      </code>
    </regTest>
  </regSuite>
</resource>

