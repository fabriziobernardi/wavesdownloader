
WAVESDOWNLOADER
---------------
Python based tool for seismological data discovery, 
downloading, pre-processing and plotting


==  Version 1.2.03  - 2013.08.08  ==

Download:
---------
http://webservices.rm.ingv.it/wavesdownloader/


INSTALL: 
-------- 

1. Please install theses packages first:
 - scipy [http://www.scipy.org/]
 - numpy [http://numpy.scipy.org/]
 - obspy [http://obspy.org/]

 - For Mac Os a dmg file for easy install, 
   including the three packages, is avaliable:

   http://dl.dropbox.com/u/3866312/ObsPy.dmg 

 
2. Instal suds module: 
   - linux: https://fedorahosted.org/suds
   - mac:   sudo easy_install -z suds 

3. Instal rdseed and add the PATH into your .profile/.bash/....
   http://www.iris.edu/forms/rdseed_request.htm

4. chmod +x wavesDownloader.py

EIDA REGISTRATION:
------------------

Please fill form at http://webservices.rm.ingv.it/ingv_ws_registration.php for automatic registration to access EIDA services


USAGE:
------
usage: wavesdownloader.py [-h] [--beg BEG] [--end END] [--len LEN] [--usr USR]
                          [--pas PAS] [--sta STA] [--net NET] [--loc LOC]
                          [--cha CHA] [--rot ROT] [--res RES] [--mode MODE]
                          [--center CENTER] [--radius RADIUS]
                          [--supCor SUPCOR] [--infCor INFCOR]
                          [--format FORMAT] [--outdir OUTDIR]
                          [--server SERVER] [--fsfile FSFILE]
                          [--rmgaps RMGAPS] [--mingap MINGAP]
                          [--maxgap MAXGAP] [--reject REJECT] [--cfreq CFREQ]
                          [--demean DEMEAN] [--bandpass BANDPASS]
                          [--highpass HIGHPASS] [--lowpass LOWPASS]
                          [--wfiltr WFILTR] [--deci DECI] [--deco DECO]
                          [--flim FLIM] [--slta SLTA] [--wcf WCF] [--pgm PGM]
                          [--pgmfile PGMFILE] [--shake SHAKE] [--sa SA]
                          [--pltmode PLTMODE] [--pltchan PLTCHAN]
                          [--pltNERT PLTNERT] [--pltazi PLTAZI]
                          [--summary SUMMARY]

Download seeds from archives, pre-process and process  data for use

optional arguments:
-------------------
  -h, --help           show this help message and exit
  --beg BEG            Begin Time. !! No defaults!! Format YYYY-MM-DDThh:mm:ss
                       (UTC Time) (e.g.: 2011-07-25T12:30:00)
  --end END            End Time. !! No defaults!! F\ormat YYYY-MM-DDThh:mm:ss
                       (UTC Time) (e.g.: 2011-07-25T12:35:00)
  --len LEN            Length of signal in seconds. !! No defaults!! Mandatory
                       option if --end not specified
  --usr USR            User name for eida !! MANDATORY OPTION, No defaults!!
  --pas PAS            Passwd for eida \!! MANDATORY OPTION, No defaults!!
  --sta STA            Station list. default=*
  --net NET            Network list. default=*
  --loc LOC            Station information location ID. default=*
  --cha CHA            Channel list. default=BHZ
  --rot ROT            Rotate horizontal components from North-East -> Radial-
                       Trasversal. Only with --mode “center”. Default
                       [Y]/N.
  --res RES            Instrument response extraction: 0=none; 1=RESP; 2=PAZ
                       (default); 3=RESP&PAZ
  --mode MODE          Area selection mode: [circular|rectangular]
                       default=circular
  --center CENTER      Lat Lon inner position for circular request. Default
                       "41.9 12.5"
  --radius RADIUS      Radius in DEGREE from innerPos to outerPos for --mode
                       circular. Default="0 10"
  --supCor SUPCOR      Max latitude and longitude for --mode rectangular.
                       Default="60 60"
  --infCor INFCOR      Min latitude and longitude for --mode rectangular.
                       Default="10 10"
  --format FORMAT      file format extraction storage
                       [SAC,SACXY,GSE1,GSE2,SH_ASC,WAV]. If format=SAC no data
                       extracted. Default=None
  --outdir OUTDIR      directory for data extraction. Default=data
  --server SERVER      servers [EIDA,IRIS,LOCAL,WEBDC]. LOCAL look for fseed
                       files stored on your local machine. Only fseed files
                       are allowed. --server "LOCAL" needs --fsfile to be
                       specified. LOCAL and external server are allowed within
                       the same request. Default="EIDA WEBDC IRIS"
  --fsfile FSFILE      fseed file name inclusive of path if path different
                       than \. Default None
  --rmgaps RMGAPS      Remove traces with gaps. default=Y
  --mingap MINGAP      Minimum gap allowed in seconds. default=0
  --maxgap MAXGAP      Maximum gap allowed in seconds. default=0
  --reject REJECT      Minimum length in percent for trace rejection.
                       default=100
  --cfreq CFREQ        Get dominant period [N]/Y.
  --demean DEMEAN      Remove mean and trend. Default=Y
  --bandpass BANDPASS  Bandpass filter "corners fimn fmax". No Defaults. E.g.:
                       "2 0.01 0.1"
  --highpass HIGHPASS  Highpass filter "corners freq". No Defaults. E.g.: "2
                       0.01"
  --lowpass LOWPASS    Lowpass filter "corners freq". No Defaults. E.g.: "2
                       0.1"
  --wfiltr WFILTR      Write new filtered files into --wfiltr path. Default=N
  --deci DECI          Decimation factor for sampling rate. Only integer
                       decimation factor allowed. Default=None
  --deco DECO          Deconvolution from instrument response [N]/Y. Requires
                       --res=[2|3]. Default=N
  --flim FLIM          Corner frequency for deconvolution filtering. Defaults
                       0.002 0.005 0.5 1
  --slta SLTA          Make Short-term/long-term average and trigs picks:
                       --slta "STA LTA ON OFF" (--sta "0.5 5 7 1.5").
                       Default=”None” STA: Short-term average LTA: Long-
                       term average ON: level trigger on OFF: level trigger
                       off
  --wcf WCF            Write characteristic function from slta into sac file
                       format [N]/Y. Only binary sac file format allowed. No
                       need to use --format option
  --pgm PGM            Peaks Ground Motion parameters. max_displacement [m],
                       max_velocity[m/s], max_acceleration[m/s^2]. Output into
                       summary3.log file. Automatically enable --sa option
                       (Spectral acceleration response). Default [N]/Y
  --pgmfile PGMFILE    Name file for shakemap. User file-name MUST end with
                       "_dat.xml" in order to be accepted by ShakeMap.
                       Default=shakeList_dat.xml
  --shake SHAKE        Write PGMs for ShakeMap. [N]/Y
  --sa SA              Modify defaults Spectral Acceleration Response
                       parameters (only if –pgm=”Y”): damping and corner
                       frequencies in Hz. Example: --sa “0.1 1 10”;
                       damping factor (0.1) and corner frequencies in Hz.
                       Spectral Acceleration Response in [m/s^2]. Defaults:
                       sa=”0.05 3.33 1.00 3.33”.
  --pltmode PLTMODE    plot traces. 0=No plot; 1=y_axe regular; 2=y_axe
                       distance from epicenter. Plots saved in pdf format, see
                       Notes for details. (Default=0). Plot names:
                       plotWavesZ.pdf for vertical; plotWavesNS.pdf and
                       plotWavesEW.pdf with --pltNERT "NE"; plotWavesT.pdf and
                       plotWavesR.pdf with --pltNERT "RT"
  --pltchan PLTCHAN    channel to plot. Default=None
  --pltNERT PLTNERT    horizontal components [NE|RT]. Default=None !! ONLY
                       with --rot=Y
  --pltazi PLTAZI      Plot traces within azimuth. Default="0 360"
  --summary SUMMARY    Print data request summary on screen. [N]/Y.

  SUMMARY-LOG FILES:
  ------------------
 
Summary.log files are automatically saved into the --outdir directory:
  
1. summary1.log  :

Includes a summary of all option used to run wavesdownloader

2. summary2.log  : 
List downloaded stations and metadata.
	Format: One line for each station.channel data. Metadata for each line: 
     		StationCode  
		Network 
		Channel 	
		LocationCode 
		BegTime 
		EndTime 
		Samp_rate 	
		dT 
		Station_lat 
		Station_lon 
		Event_lat 
		Event_lon 
		Epicentral_distance (degree) 
		Azimut 
		Back_azimuth 	
		Epicentral_distance (km)

	Example:
     	ASQU  IV HHE -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 43.797  11.789  44.480  10.033  159.811 1.437   117.768 298.987 
	ASQU  IV HHN -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 43.797  11.789  44.480  10.033  159.811 1.437   117.768 298.987 
	ASQU  IV HHZ -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 43.797  11.789  44.480  10.033  159.811 1.437   117.768 298.987 
	BDI      IV HHE -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 44.062  10.597  44.480  10.033  64.692  0.582   135.664 316.056 
	BDI      IV HHN -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 44.062  10.597  44.480  10.033  64.692  0.582   135.664 316.056 
	BDI      IV HHZ -- 2012-01-27T14:53:00.00Z   2012-01-27T14:55:00.00Z   100.00   0.0100       12001 44.062  10.597  44.480  10.033  64.692  0.582   135.664 316.056 

3. summary3.log  : 
List downloaded stations, metadata, PGMs, central frequency and picker values. 2 Lines of format explaining header.
	Format: One line for each station.channel data. Metadata and values for each line: 
     		StationCode  
		Network 
		Channel 	
		LocationCode 
		Station_lat 
		Station_lon 
		Event_lat 
		Event_lon 
		Epicentral_distance (km) 
		Azimut
		PeakGroundDisplacement [m]
		PeakGroundVelocity [m/s]
		PeakGroundAcceleration [m/s^2]
		List of Spectral Acceleration Response at different corner frequencies [m/s^2] (may be empty)
		Central Frequencies [Hz] (may be empty)
		Short-term average
		Long-term average
		Picker trigger on value
		Picker trigger off value
		Picking list (Sample after begin trace)

	Examples:
     	ASQU  IV    HHE   --      43.797  11.789  44.480  10.033     159.8 117.768         8.530e-05         2.395e-04         4.507e-03                    1.230e-02 3.142e-03 2.264e-04      1.528e-01   -1.00   -1.00   -1.00   -1.00  -1
	

      	BOB   IV    HHZ   --      44.768   9.448  44.480  10.033      56.4 304.766         2.873e-04         1.800e-03         3.392e-02                    6.413e-02 1.634e-02 1.560e-03      1.032e+00    1.00    7.00    5.00    1.00  [2688 3251][3657 4070]
	
	Note: -1.00 values means that shrt/long term average and trigger are off

  !!! FAILURES:
  --------------
  --server        Servers busy or not responding may return into script failure.
                  run the script later or remove the server which causes error.

  NOTES:
  ------
  --cha           Wildcard allowed only for one channel. e.g.: "BH*" or "HH*"
                  but not "BH* HH*". Use "BHZ BHN BHE HHZ HHN HHE" instead.
  --reject 100    means only traces with full required length are hold
  --reject 10     means all traces that are only a 10% or shorter with
                  respect to the total required length are removed
  --rot           When --rot==Y and --reject < 100,              
                  rotation of the horizontal component may fail.
                  Rotation requires identical record length of the
                  horizontal components. Thus  --rot==Y force --reject 100.
                  It may occurs that --rot="Y" and --reject 100 do not result true
                  because of files synchronization.
  --server "IRIS EIDA"
                  Generally EIDA provides real-time data while IRIS not
  --pltmode       When enabled, this option also save the plots into pdf file format into 
                  --outdir path. Plot names: plotWavesZ.pdf for vertical; plotWavesNS.pdf
                  and plotWavesEW.pdf with --pltNERT "NE"; plotWavesT.pdf and plotWavesR.pdf
                  with --pltNERT "RT" 
                  When --slta != None and pltmode activated, the picks are plotted automatically
  --pgm --slta    Applied after deconvolution and filtering  
 

  EXAMPLES:
  ---------

  1. Circular download.
  ---------------------
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-01-29T17:41:00 --end 2011-01-29T17:45:00 --center "47.56 18.34" --radius "0 6" 

  2. Circular Download with server EIDA selected and plot (y-axe = Distance [km]).
  --------------------------------------------------------------------------------
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-05-26T11:35:00 --len 300 --center "42.94 11.05" --radius "0 1.8"  --server "EIDA" --res 3 --pltmode 2 --pltcha B

  3. Rectangular Download with network, channel selectd and plot.
  --------------------------------------------------------------- 
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-01-29T06:55:00 --end 2011-01-29T07:15:00 --mode rectangular --infCor "40 -10" --supCor "85 30" --net "MN II" --cha "BH*" --pltmode 1 --pltcha B

  4. Rectangular Download with bandpass filter from IRIS, no user and password required. 
  --------------------------------------------------------------------------------------
  ./wavesdownloader.py --beg 2011-04-01T13:29:00 --end 2011-04-01T13:49:00 --mode rectangular --infCor "20 10" --supCor "60 60" --server "IRIS" --net "MN GE II" --cha "BH*" --pltmode 1 --bandpass "2 0.01 0.02" --pltcha B

  5. Circulare Download with rotation to GCP and azimuthal selected plot. Lopass filtered data ar stored into "filterd" subdirectory. End timewindow 600 second after begin Time.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-07-17T18:30:00 --len 600 --center "45.01 11.41" --radius "0 2" --cha "BH*" --pltmode 2 --rot "Y" --pltNERT "RT" --pltazi "0 180" --lowpass "4 0.5" --wfiltr "filtered" --format SAC --pltcha B

  6. Circulare Download with multiple channel list selection.
  -----------------------------------------------------------
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-07-17T18:30:00 --len 600 --center "45.01 11.41" --radius "0 2" --server "EIDA" --cha "BHZ BHN BHE HHZ HHN HHE" 

  7. Circular Download with slta picking and lowpass filter.
  ----------------------------------------------------------
  ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2011-07-17T18:29:00 --end 2011-07-17T18:34:00 --center "45.01 11.41" --radius "0 1" --server "EIDA" --cha "BHZ" --pltmode 2  --pltcha B --cfreq "Y" --slta "1 5 4 1" --lowpass "4 1" --wfiltr filtered --format SAC

  8. Circular Download from IRIS server including local fseed file as a data source. Instrument response deconvolution and user specified corner frequencies for deconvolution. No user and Password required. Default --res 2.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ./wavesdownloader.py --beg 2011-07-17T18:29:00 --end 2011-07-17T18:34:00 --center "45.01 11.41" --radius "0 20" --server "IRIS LOCAL" --fsfile "mypath/myfile.fseed" --net "II MN IU" --cha "BHZ" --pltmode 2  --cfreq "Y" --slta "1 5 4 1" --lowpass "4 1"  --deco Y --flim "0.01 0.05 0.1 1" --pltcha B

  9. ShakeMap configuartion. Corner frequencies limits for deconvolution should be adapted for high frequencies. Pgm values stored into user specified file "ShakePga_dat.xml".
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2012-05-29T10:54:00 --len 200 --center "44.89 11.01" --radius "0 4" --server EIDA --cha "HH*" --res 3 --deco Y --pgm Y --shake Y --pgmfile ShakePga_dat.xml --flim "0.05 0.1 20 40"
