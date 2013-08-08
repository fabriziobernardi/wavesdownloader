#!/usr/bin/env python
# encoding: utf-8

import argparse,sys
import os.path

def parseMyLine():

  version = './wavesdownloader1.0.py'

  examples = """

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
 


  EIDA REGISTRATION:
  ------------------

  Please fill form at http://eida.rm.ingv.it/ingv_ws_registration.php for automatic registration
  to access EIDA services



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


  5. Circulare Download with rotation to GCP and azimuthal selected plot. Lopass filtered data ar stored into \"filterd\" subdirectory. End timewindow 600 second after begin Time.
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


  9. ShakeMap configuartion. Corner frequencies limits for deconvolution should be adapted for high frequencies. Pgm values stored into user specified file \"ShakePga_dat.xml\".
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   ./wavesdownloader.py --usr user@network.net --pas myPassword --beg 2012-05-29T10:54:00 --len 200 --center "44.89 11.01" --radius "0 4" --server EIDA --cha "HH*" --res 3 --deco Y --pgm Y --shake Y --pgmfile ShakePga_dat.xml --flim "0.05 0.1 20 40"
  
  """


  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='Download seeds from archives, pre-process and process  data for use',epilog=examples)

  
  ############################
  # ---- optionals
  #
  # data type
  parser.add_argument('--beg', default='None', help='Begin Time. !! No defaults!! Format YYYY-MM-DDThh:mm:ss (UTC Time) (e.g.: 2011-07-25T12:30:00)')
  parser.add_argument('--end', default='None', help='End Time. !! No defaults!! F\ormat YYYY-MM-DDThh:mm:ss (UTC Time) (e.g.: 2011-07-25T12:35:00)')
  parser.add_argument('--len', default='None', help='Length of signal in seconds. !! No defaults!! Mandatory option if --end not specified')
  parser.add_argument('--usr', help='User name for eida !! MANDATORY OPTION, No defaults!!')
  parser.add_argument('--pas', help='Passwd for eida \!! MANDATORY OPTION, No defaults!!')
  parser.add_argument('--sta',default='*',help='Station list. default=*')
  parser.add_argument('--net',default='*',help='Network list. default=*')
  parser.add_argument('--loc',default='*',help='Station information location ID. default=*')
  parser.add_argument('--cha',default='BHZ',help='Channel list. default=BHZ')
  parser.add_argument('--rot',default='N',help='Rotate horizontal components from North-East -> Radial-Trasversal. Only with --mode “center”. Default [Y]/N. ')
  parser.add_argument('--res',default='2',
                      help='Instrument response extraction: 0=none; 1=RESP; 2=PAZ (default); 3=RESP&PAZ')
  #
  # request mode
  parser.add_argument('--mode', default='circular', 
                      help='Area selection mode: [circular|rectangular] default=circular')
  parser.add_argument('--center',default='0 0', 
                      help='Lat Lon inner position for circular request. Default "41.9 12.5"')
  parser.add_argument('--radius', default='0 10', 
                      help='Radius in DEGREE from innerPos to outerPos for --mode circular. Default="0 10"')
  parser.add_argument('--supCor', default='60 60', 
                      help='Max latitude and longitude for --mode rectangular. Default="60 60"')
  parser.add_argument('--infCor', default='10 10', 
                      help='Min latitude and longitude for --mode rectangular. Default="10 10"')
  #
  # storage
  parser.add_argument('--format',default='None', 
                      help='file format extraction storage [SAC,SACXY,GSE1,GSE2,SH_ASC,WAV]. If format=SAC no data extracted. Default=None')
  parser.add_argument('--outdir',default='data', help='directory for data extraction. Default=data')
  parser.add_argument('--server',default='EIDA WEBDC IRIS', help='servers [EIDA,IRIS,LOCAL,WEBDC]. LOCAL look for fseed files stored on your local machine. Only fseed files are allowed. --server "LOCAL" needs --fsfile to be specified. LOCAL and external server are allowed within the same request. Default="EIDA WEBDC IRIS"')
  parser.add_argument('--fsfile',default='None',help='fseed file name inclusive of path if path different than \. Default None')
  #
  # quality
  parser.add_argument('--rmgaps', default='Y', help='Remove traces with gaps. default=Y')
  parser.add_argument('--mingap', default='0', help='Minimum gap allowed in seconds. default=0')
  parser.add_argument('--maxgap', default='0', help='Maximum gap allowed in seconds. default=0')
  parser.add_argument('--reject', default='100', help='Minimum length in percent for trace rejection. default=100')
  parser.add_argument('--cfreq', default='N', help="Get dominant period [N]/Y.")
  #
  # filter: bandpass, highpass, lowpass, mean and trend, 
  parser.add_argument('--demean',default='Y', help='Remove mean and trend. Default=Y')
  parser.add_argument('--bandpass',default='0', help='Bandpass filter "corners fimn fmax". No Defaults. E.g.: "2 0.01 0.1"')
  parser.add_argument('--highpass',default='0', help='Highpass filter "corners freq". No Defaults. E.g.: "2 0.01"')
  parser.add_argument('--lowpass',default='0', help='Lowpass filter "corners freq". No Defaults. E.g.: "2 0.1"')
  parser.add_argument('--wfiltr',default='N', 
                      help='Write new filtered files into --wfiltr path. Default=N')
  parser.add_argument('--deci',default='None', help='Decimation factor for sampling rate. Only integer decimation factor allowed. Default=None')
  parser.add_argument('--deco',default='N', help='Deconvolution from instrument response [N]/Y. Requires --res=[2|3]. Default=N')
  parser.add_argument('--flim',default='0.002 0.005 0.5 1', help='Corner frequency for deconvolution filtering. Defaults 0.002 0.005 0.5 1')
  parser.add_argument('--slta',default='None', help='Make Short-term/long-term average and trigs picks: --slta "STA LTA ON OFF" (--sta "0.5 5 7 1.5"). Default=”None”\n STA:  Short-term average\nLTA: Long-term average\nON: level trigger on\nOFF: level trigger off')
  parser.add_argument('--wcf', default='N', help='Write characteristic function from slta into sac file format [N]/Y. Only binary sac file format allowed. No need to use --format option')
  parser.add_argument('--pgm',default='N', help='Peaks Ground Motion parameters. max_displacement [m], max_velocity[m/s], max_acceleration[m/s^2]. Output into summary3.log file.  Automatically enable --sa option (Spectral acceleration response). Default [N]/Y')  
  parser.add_argument('--pgmfile',default='shakeList_dat.xml', help='Name file for shakemap. User file-name MUST end with \"_dat.xml\" in order to be accepted by ShakeMap. Default=shakeList_dat.xml')
  parser.add_argument('--shake',default='N', help='Write PGMs for ShakeMap. [N]/Y')
  parser.add_argument('--sa',default='0.05 3.33 1.0 0.33', help='Modify defaults Spectral Acceleration Response parameters (only if –pgm=”Y”): damping and corner frequencies in Hz. Example: --sa “0.1 1 10”; damping factor (0.1) and corner frequencies in Hz. Spectral Acceleration Response in [m/s^2]. Defaults: sa=”0.05 3.33 1.00 3.33”.') 
  #
  # plotmode
  parser.add_argument('--pltmode',default='0',
                     help='plot traces. 0=No plot; 1=y_axe regular; 2=y_axe distance from epicenter. Plots saved in pdf format, see Notes for details. (Default=0). Plot names: plotWavesZ.pdf for vertical; plotWavesNS.pdf and plotWavesEW.pdf with --pltNERT "NE"; plotWavesT.pdf and plotWavesR.pdf with --pltNERT "RT"')
  parser.add_argument('--pltchan',default='None',help='channel to plot. Default=None')
  parser.add_argument('--pltNERT',default='None',help='horizontal components [NE|RT]. Default=None  !! ONLY with --rot=Y')
  parser.add_argument('--pltazi',default='0 360',help='Plot traces within azimuth. Default="0 360"')
  parser.add_argument('--summary',default='N',help='Print data request summary on screen. [N]/Y.')
  

  ###################################
  # ---- parse
  args=parser.parse_args()

  if args.pgm == "Y":
     print "Warning. Remember to set the appropriate limit corner frequencis for deconvolution (i.e.: highpass)"

  if args.summary == "Y":
     print "\n\nSUMMARY:\n--------\n"
     print args,"\n"

 
  if  args.deci != "None":
      args.deci = int(args.deci)


  return args


def checkConsistency(self):

    ntws = self.net.split(' ')
    chas = self.cha.split(' ')

    if self.server[3] == 1 and len(chas) >=2:
       print "WEBDC servers allows only one channel request or a general wildcard;  i.e.: --cha BHZ  or --cha \"BH*\"."
       print "No multiple networs request is allowed; i.e.: --cha \"BHZ HHZ\""
       sys.exit()

    if self.server[3] == 1 and len(ntws) >=2:
       print "WEBDC servers allows only one network request or a general wildcard (default value); i.e.: --net MN or let default value."
       print "No multiple networs request is allowed; i.e.: --net \"MN IV\""
       sys.exit()

    if self.wfiltr != "N" and self.format == "None":
       print "Please set output file format using --format"
       sys.exit()

    if self.shake == "Y" and self.pgmfile != "shakeList_dat.xml":
       a = self.pgmfile[-8:]
       if a != "_dat.xml":
          print "ShakeMap file name MUST end with \"_dat.xml\" in order to be accepted by ShakeMap"
          sys.exit()

    if self.deco == "Y" and self.res == "0":
       print "You require poles and zeros to be extracted for deconvolution. Exit"
       sys.exit()

    if self.deco == "Y" and self.res == "1":
       print "You require poles and zeros to be extracted for deconvolution. Exit"
       sys.exit()

    if self.pltmode=="2" and self.mode=="rectangular":
       print "Arguments --pltmode = " + self.pltmode + \
             " and --mode = " + self.mode + \
             " are incompatibles"
       sys.exit()

    if self.rot=="Y" and self.mode=="rectangular":
       print "Arguments --rot = " + self.rot + \
             " and --mode = " + self.mode + \
             " are incompatibles"
       sys.exit()

    if self.mode=="rectangular" and self.pltNERT =="RT":
       print "Arguments --mode = " + self.mode + \
             " and --pltNERT = " + self.pltNERT + \
             " are incompatibles"
       sys.exit()

    if self.rot=="N" and self.pltNERT =="RT":
       print "Arguments --rot = " + self.rot + \
             " and --pltNERT = " + self.pltNERT + \
             " are incompatibles"
       sys.exit()

    if self.beg=="None":
       print "no begin time specified. Check --beg option"
       sys.exit(0)

    if self.len=="None" and self.end=="None":
       print "no end or length time specified. Check --end/--len option"
       sys.exit(0)

    if self.beg=="None" and self.len=="None":
       print "no begin time specified. Check --end option"
       sys.exit(0)

    #test if frequencies for shakemap are set
    if(self.shake == "Y"):
      self.sa == "0.5 3.33 1.0 0.33"
 
    #force --reject=100 if --rot="Y"
    if self.rot=="Y":
       self.reject="100"

 
    #trigger parameters for Sta/Lta must be 4: Sta Lta On Off
    if self.slta!="None":
       nr = self.slta.split(' ')
       if len(nr) != 4:
          print "check parameters for --slta"
          sys.exit() 
       if eval(nr[3]) >= eval(nr[2]):
          print "trigger on must be greather than trigger off value"
          sys.exit()
       if eval(nr[0]) >= eval(nr[1]):
          print "Short-term average must be smaller than Long-term average"
          sys.exit()

    # plotting channel
    if self.pltchan == "None" and self.pltmode != "0":  
       print "Specify channel to plot using --pltchan. E.g.: --pltchan B"
       sys.exit()

    lista_pltchan = self.pltchan.split(' ')
    if len(lista_pltchan) >= 2:
       print "Only one channel allowed for --pltchan"
       sys.exit()
    plt=0
    if self.pltmode != "0":
       lista_chan = self.cha.split(' ')
       for i in range(len(lista_chan)):
          if lista_chan[i][0] == self.pltchan:
             plt=1
    if plt == 0 and self.pltmode != "0":
       print "check --cha and --pltchan args: --cha", self.cha, " --pltchan", self.pltchan
       sys.exit()

    if self.fsfile != "None":
       aa=os.path.exists(self.fsfile)
       if aa == False:
          print "File --fsfile", self.fsfile, "does not exists"
          sys.exit()

    # test if rdseed exists
    if os.system("which rdseed") == 256:
       print "rdseed not found"
       sys.exit()
       
