################################################################
#
# Script wavedDownloader: download seismic data and metadata from archives
#
# HELP: type ./wavesdownloader --help
#
################################################################
    
    
#################################################################
# ----  A. Import classes and functions ----                    #
import math, os, sys, optparse
from obspy.signal import bwith
from obspy.core import read, UTCDateTime, trace
from obspy.iris import Client as IClient
from myUsefullFuncs import *
from EidaWebServices import *
from EidaSpeaker import *
from shutil import *
from copy import deepcopy
from myParser import parseMyLine
from xml.dom.minidom import parseString
from operator import itemgetter
from obspy.signal import filter #, rotate
from plotWaves import plotWaves
import os.path
import scipy.stats as ss
import matplotlib.pyplot as plt
import pylab
import xml.parsers.expat
from myParser import checkConsistency,parseMyLine
from pyShake import export4ShakeMap,writeShake
from pyArcLink import getInventoryViaArcLink,getDataViaArcLink,writeWbDcStation
from myUsefullFuncs import decimateStream

    
def wavesdownloader(args):



    #################################################################
    # ---- Check if internet connection is active 
    #
    # check servers
    args.server=list2servers(args.server,'N')
    # Do not apply if only LOCAL is active
    if (args.server[0] == 1 or args.server[1] == 1 or args.server[3] == 1 or args.server[4] == 1):
       try:
          urllib2.urlopen("http://google.com", timeout=2)
       except urllib2.URLError:
          print "No internet connection"
          sys.exit()
    
     
    #################################################################
    # ----  C. Initialize variables ----                            #
    dataStreamEida = Stream()
    dataStreamIris = Stream()
    dataStreamLoca = Stream()
    dataStreamWbDc = Stream()
    dataStream     = Stream()
    center=args.center.split(' ')
    grradius=args.radius.split(' ')
    kmradius=args.radius.split(' ')
    ev_lat=eval(center[0])
    ev_lon=eval(center[1])
    kmradius[0]=eval(kmradius[0])*100
    kmradius[1]=eval(kmradius[1])*100
    bbox=getBBox(args.supCor,args.infCor) #minlat minlon maxlat maxlon
    aFormat="fseed"
    aFORMAT="FSEED"
    irisClient = IClient()
    ID = "0"

    # check consistency of arguments
    checkConsistency(args)

    # define t1 and t2
    if args.end=="None":
       t1 = UTCDateTime(args.beg)
       t1.getTimeStamp()
       t2 = t1+int(args.len)
       t2= str(t2)[:19] #this must be a string for
       args.end=t2
    else:
       t1 = UTCDateTime(args.beg)
       t2 = UTCDateTime(args.end)
       if t1 >= t2:
          print "Wrong begin and end time entries"
          sys.exit()


    # make outdir if not exist (from myUsefullFuncs)
    if args.outdir != ".":
       mkdir(args.outdir)
    # if filtering require data writing
    if args.wfiltr == "Y":
       mkdir(args.outdir + os.sep + "_f")

    # write  summary
    makeSummary(1,dataStream,args)
    

    # check for local fseed archive
    if args.server[2] == 1 and args.fsfile == "None":
       print "local fseed file non spcified. Check --fsfile option"
       sys.exit(0)
    
    #################################################################
    # ----  D. Download waveforms (fseed and stream)
    # if eida is on
    if args.server[0] == 1:

      # Convert some args for eida syntax 
      args.net=reformatNetStaList(args.net,"eida")
      args.sta=reformatNetStaList(args.sta,"eida")
      args.cha=reformatChaStaList(args.cha,"eida")
    
      # initialize eida requestor 
      user=INGV_requestor(args.usr,args.pas)
    
      # download
      print "\n \nDownloading from eida"
      if args.mode == "circular":
        (downloadPath,ID) = user.run_circular_query( \
                            args.net,args.sta,args.cha, \
                            center[0],center[1],kmradius[0],kmradius[1], \
                            args.beg,args.end,aFORMAT)
      else: # i.e.: rectangular
        (downloadPath,ID) = user.run_rectangular_query( \
                            args.net,args.sta,args.cha, \
                            bbox[0],bbox[1],bbox[2],bbox[3], \
                            args.beg,args.end,aFORMAT)
    
      #set name and location of the fseed 
      archiveFile = downloadPath + os.sep + ID + "_data.tgz"
      (root,seed)=grabIngvEidaArchive(archiveFile,aFormat)
    
      # get stream
      try: 
        dataStreamEida = read(seed)
      except:
        print "no data found or no response from Eida server"

    
    # if iris is on
    if args.server[1] == 1:
    
       # Convert some args for eida syntax 
       args.net=reformatNetStaList(args.net,"iris")
       args.sta=reformatNetStaList(args.sta,"iris")
       args.cha=reformatNetStaList(args.cha,"iris")
    
       # initialize downloader
       print "\n \nDownloading from iris"
       if args.mode == "circular":
          response = irisClient.availability( \
                     network=args.net, station=args.sta, channel=args.cha, \
                     location=args.loc,starttime=t1, endtime=t2, \
                     lat=center[0], lon=center[1], minradius=grradius[0], maxradius=grradius[1])

       else: # i.e.: rectangular
          IrisBox = setIrisRectBox(bbox)
          response = irisClient.availability( \
                     network=args.net, station=args.sta, channel=args.cha, \
                     location=args.loc,starttime=t1, endtime=t2,\
                     minlat=IrisBox[0], minlon=IrisBox[1], maxlat=IrisBox[2], maxlon=IrisBox[3])
    
       # Download
       try:
           dataStreamIris = irisClient.bulkdataselect(response)
           # here save mseed file format
           dataStreamIris.write(args.outdir + os.sep + 'iris.' + ID + '_data.mseed',format='MSEED', encoding='STEIM2')
       except:
           print "IRIS bulkdataselect returns False. No data from IRIS\n\n"
    
    
    #
    # if local is on
    if args.server[2] == 1:
       print "\n \nExtracting from local fseed"
       dataStreamLoca=read(args.fsfile)


    # if ARClink - WEBDC is on
    if args.server[3] == 1:
    
       print "\n \nDownloading from WEBDC via ArcLink"
       # Convert some args for eida syntax 
       args.net=reformatNetStaList(args.net,"iris")
       args.sta=reformatNetStaList(args.sta,"iris")
       args.cha=reformatNetStaList(args.cha,"iris")

       # get station list available
       Inventory=getInventoryViaArcLink(t1,t2,center,grradius,bbox,args)
       # download data
       dataStreamWbDc=getDataViaArcLink(t1,t2,Inventory,args)
       if len(dataStreamWbDc) > 0:
          dataStreamWbDc.write(args.outdir + os.sep + 'webdc.' + ID + '_data.mseed',format='MSEED', encoding='STEIM2')
       
    ############################################################
    # Check if only empty data
    if(len(dataStreamIris) + len(dataStreamEida) + len(dataStreamLoca) + len(dataStreamWbDc)<=0):
      print "\nNo data found! Exit!"
      sys.exit()

    ############################################################
    # ----  E. data to sac (or other formats)
    
    # trim data
    if args.beg!="None" or  args.end!="None":
       Tb = UTCDateTime(args.beg)
       Te = UTCDateTime(args.end)
       dataStreamIris.trim(starttime=Tb, endtime=Te)
       dataStreamEida.trim(starttime=Tb, endtime=Te)
       dataStreamLoca.trim(starttime=Tb, endtime=Te)
       dataStreamWbDc.trim(starttime=Tb, endtime=Te)
    
    # find gaps and remove those traces
    if args.rmgaps=="Y":
       dataStreamIris = removeGaps(dataStreamIris, args.mingap, args.maxgap, verbose="true")
       dataStreamEida = removeGaps(dataStreamEida, args.mingap, args.maxgap, verbose="true")
       dataStreamLoca = removeGaps(dataStreamLoca, args.mingap, args.maxgap, verbose="true")
       dataStreamWbDc = removeGaps(dataStreamWbDc, args.mingap, args.maxgap, verbose="true")
    
    # Remove traces shorter than expected tolerance
    args.reject=eval(args.reject)
    if args.reject <= 100:
       dataStreamIris=removeShortTraces(dataStreamIris,args.reject,Tb,Te)
       dataStreamEida=removeShortTraces(dataStreamEida,args.reject,Tb,Te)
       dataStreamLoca=removeShortTraces(dataStreamLoca,args.reject,Tb,Te)
       dataStreamWbDc=removeShortTraces(dataStreamWbDc,args.reject,Tb,Te)
    
    # Remove mean and trend if required
    if args.demean == "Y":
       dataStreamIris=removeMeanTrend(dataStreamIris)
       dataStreamEida=removeMeanTrend(dataStreamEida)
       dataStreamLoca=removeMeanTrend(dataStreamLoca)
       dataStreamWbDc=removeMeanTrend(dataStreamWbDc)

    # Decimation if required
    if args.deci != "None":
       dataStreamIris=decimateStream(dataStreamIris,args.deci)
       dataStreamEida=decimateStream(dataStreamEida,args.deci)
       dataStreamLoca=decimateStream(dataStreamLoca,args.deci)
       dataStreamWbDc=decimateStream(dataStreamWbDc,args.deci)
    
    
    ############################################################
    # ----  F. metadata, response, and paz files and update header
    #          for arcklink data Paz already exists. Resp file can't 
    #          be downloaded now (12.10.2012)
    
    # eida - very easy
    if args.server[0] == 1:
       #if args.res != "0": # and args.reqFileFormat != "MSEED":

       # first test if fseed file exists
       aa = os.path.isfile(seed)
       if aa == "False":
          print "No data found in fseed file from EIDA"
       else:
          (respFiles, pazFiles) = extractResponse(seed,args.res,args.outdir)
          if args.res == "2" or  args.res == "3":
            dataStreamEida = addPazStats(dataStreamEida,args.outdir,pazFiles)
          dataStreamEida = updateStats(dataStreamEida,args.outdir,"rdseed.stations",ev_lat,ev_lon)
          try:
            shutil.move(seed,args.outdir + os.sep + 'eida.' + ID + '_data.fseed')
          except:
            pass
          try:
            shutil.move(args.outdir + os.sep + 'rdseed.stations',args.outdir + os.sep + 'eida_rdseed.stations')
          except:
            pass


    # local same than eida  - very easy
    if args.server[2] == 1:
       #if args.res != "0":
       (respFiles, pazFiles) = extractResponse(args.fsfile,args.res,args.outdir)
       if args.res == "2" or args.res == "3":
          dataStreamLoca = addPazStats(dataStreamLoca,args.outdir,pazFiles)
       dataStreamLoca = updateStats(dataStreamLoca,args.outdir,"rdseed.stations",ev_lat,ev_lon)
       dataStreamLoca = purgeListStation(dataStreamLoca,args,'d')
       shutil.move(args.outdir + os.sep + 'rdseed.stations',args.outdir + os.sep + 'local_rdseed.stations')   
    
    # iris - longer
    if args.server[1] == 1:
       pazFiles = []
       temp_iris = open(args.outdir + os.sep + "tmp_iris.station","w")   
       # here store lat lon staz locId for later update of iris stream
    
       for i in range(len(dataStreamIris)):
         n = dataStreamIris[i].stats['network']
         s = dataStreamIris[i].stats['station']
         l = dataStreamIris[i].stats['location']
         c = dataStreamIris[i].stats['channel']
         nameresp = "RESP." + n + "." + s + "." + l + "." + c 
         namepaz  = "SAC.PZs." + n + "." + s + "." + c
    
         # get metadata station latitude and longitude
         meta = irisClient.station(network=n, station=s, location=l, channel=c, starttime=t1, endtime=t2)
         (lat,lon) = getXmlTagData(meta)
         # update temp_iris
         temp_iris.write(s + " " + n + " " + lat + " " + lon + "0.0\n")
    
         # write resp files
         if args.res == "1" or args.res == "3":
             irisClient.saveResponse(filename=args.outdir + os.sep + nameresp ,network=n, station=s, location=args.loc, channel=c,\
                 starttime=t1, endtime=t2, format='RESP')
    
         if args.res == "2" or args.res == "3":
             sacpz = irisClient.sacpz(network=n, station=s, location=args.loc, channel=c, starttime=t1, endtime=t2)
             sacpz = sac4sac(sacpz)
             f = open(args.outdir + os.sep + namepaz, 'w')
             f.write(sacpz)
             f.close()     # close close close!!!! porcoIddio che mi dimentico sempre!!!
             pazFiles.append(namepaz)
    
       # lose temp_iris
       temp_iris.close()
       
       # update stream
       dataStreamIris = updateStats(dataStreamIris,args.outdir,"tmp_iris.station",ev_lat,ev_lon)
       if args.res == '2' or  args.res == '3':
          dataStreamIris = addPazStats(dataStreamIris,args.outdir,pazFiles)

    if args.server[3] == 1:

       # Write webdc.stations file and extract PZ file
       #   and update lat lon and event loc into statz for consistency
       dataStreamWbDc=writeWbDcStation(dataStreamWbDc,args)

       if args.res == "2" or args.res == "3":
           PzFileFromStat(dataStreamWbDc,args)
           print "\nWarning, RESP files can not be downloaded from WebDC vie ArcLink\n"
       if args.res == "1":
           print "\nWarning, RESP files can not be downloaded from WebDC vie ArcLink\n"

    #############################################################
    ## ---- G. Join all traces and write mseed files with original data
    for i in range(len(dataStreamEida)):
           dataStream.append(dataStreamEida[i])
    for i in range(len(dataStreamIris)):
           dataStream.append(dataStreamIris[i])
    for i in range(len(dataStreamLoca)):
           dataStream.append(dataStreamLoca[i])
    for i in range(len(dataStreamWbDc)):
           dataStream.append(dataStreamWbDc[i])
    # Stop and exit id no data downloaded
    if len(dataStream) == 0:
       print "\n\nNo data available!\n"
       sys.exit()

    #############################################################
    ## ---- join stations files
    files = []
    if (args.server[0] == 1):
       if(args.outdir + os.sep + "tmp_iris.station"  == True):
         files.append(args.outdir + os.sep + "tmp_iris.station")
    if (args.server[1] == 1):
       if(args.outdir + os.sep + "eida_rdseed.stations" == True):
          files.append(args.outdir + os.sep + "eida_rdseed.stations")
    content = ''
    for f in files:
       content = content + '\n' + open(f).read()
    open(args.outdir + os.sep + 'list.stations','w').write(content)
    
 
    #############################################################
    ## ---- H. Make deconvolution of instrument
    if args.deco == "Y":
       dataStream = removeInstrument(dataStream,args)

    #############################################################
    ## ----  I. Rotate orizontal to GCP
    if args.rot == "Y":
       rotatDataStream = rotateToGCP(dataStream)
       # join horizontal with rotated
       dataStream=join_NERT(dataStream,rotatDataStream)

    #############################################################
    # Write fseed to sac
    if(args.format!="None"):
      RsacFilesEida = fromFseed2sac(dataStream, args.format, args.outdir, args.format)
      for i in range(len(RsacFilesEida)):
         lat=dataStream[i].stats['stla']
         lon=dataStream[i].stats['stlo']
         ev_lat=dataStream[i].stats['evla']
         ev_lon=dataStream[i].stats['evlo']
         ok = updateSacHeader(RsacFilesEida[i],args.outdir,lat,lon,ev_lat,ev_lon)

    #############################################################
    ## ---- L. Write mseed to store semi-processed data.
    #  ---- and other output files
    # if needs to repeat analysis with different parameters on these data just add option 
    # --redo "Y" to your data request line. --server and --res will be automatically disabled
    # and the following mseed file will be loaded. Do not change the name of this file if you want to use 
    # --redo "Y"
    # analysis includes only --filter --cFreq --Sta/Lta --deco 
    #dataStream.write(args.outdir + os.sep + 'downloadedData.mseed', format='MSEED',encoding='FLOAT64')
    # and make summary level 2 (write stats.elements not writable on mseed
    makeSummary(2,dataStream,args)


    ############################################################
    # ----  Write output files
    # kml file station for google
    createKML(dataStream,args.outdir)
     


    ############################################################
    # ---- START DATA ANALYSIS:

    ############################################################
    # ----  M: filter data if required (deafult=none) 
    if args.bandpass == "0" and args.lowpass == "0" and args.highpass == "0":
       pass
    else:
       dataStream=FilterData(dataStream, args.bandpass, args.highpass, args.lowpass)

    
    ############################################################# 
    ## ---- N. Write processed data with filter . This include also rotated filtered data 
    if args.wfiltr != "N":
       outP = args.outdir + os.sep + args.wfiltr
       mkdir(outP)
       FsacFiles = fromFseed2sac(dataStream, args.format, outP, args.format)
    

    #############################################################
    ## ----  O. compute central frequency, Sta/Lta
    # Initialize stats for this section
    dataStream=initStats(dataStream)

    # central frequency
    """
    The period is determined as the period of the maximum value of the
    Fourier amplitude spectrum.
    """
    if args.cfreq=="Y":
       dataStream=cFreqStream(dataStream) 

    # pick using sta/lta
    staLtaStream=Stream()
    if args.slta!="None":
       staLtaStream=StaLta(dataStream,args.slta)
       staLtaStream=trig(staLtaStream,args.slta)
       staLtaStream.write(args.outdir + os.sep + 'picks.mseed', format='MSEED',encoding='FLOAT64')
       dataStream=syncStat(staLtaStream,dataStream)
       # if required to write 
       if args.wcf == "Y":
          SL = fromFseed2sac(staLtaStream,"SAC",args.outdir,'slt')

    # get PGMs:
    if args.pgm=="Y":
       dataStream=get_PGMs(dataStream,args)
       if(args.shake == 'Y'):
         (xmlHeader,shakeLines)=export4ShakeMap(dataStream) 
         writeShake(xmlHeader,shakeLines,args)


    # write summary level 3: data analysis
    makeSummary(3,dataStream,args)


    ############################################################
    # ----  P. Plot 
    args.pltmode = int(args.pltmode)
    if args.pltmode!=0:   
       plotWaves(dataStream,args.pltmode, \
                 kmradius, args.mode,args.pltchan, \
                 args.pltNERT,args.pltazi, \
                 staLtaStream,args.slta, args.outdir, args.rot)
