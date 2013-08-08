from obspy.core import read, UTCDateTime, trace
from obspy.core.stream import Stream
from obspy.sac import SacIO,attach_paz
from obspy.signal import seisSim,rotate_NE_RT,recSTALTA,triggerOnset,cornFreq2Paz
from obspy.signal.util import nextpow2, smooth
from scipy.signal import detrend
from xml.dom.minidom import parseString
from math import *
from scipy.integrate import quad,cumtrapz
from xml.dom import minidom, Node
from copy import deepcopy, copy
from scipy import fftpack
from mypsd import cfrequency
import subprocess
import numpy as np
import os,sys
import shutil
import pylab
import kmlmodule
from scipy.signal import convolve

def setIrisRectBox(bbox):

    out = np.array([0.,0.,0.,0.])
    out[0] = bbox[0]
    out[1] = 360 - bbox[1]
    out[2] = bbox[2]
    out[3] = 360 - bbox[3]

    return out

def reloadStats(tr,args,file):

    log = open(args.outdir + os.sep + file,"r")
    line=log.readlines()

    for i in range(len(tr)):
       sta=tr[i].stats['station']
       net=tr[i].stats['network']
       cha=tr[i].stats['channel']
       npt=tr[i].stats['npts']
       loc= tr[i].stats['location']

       a=line[i].rstrip().split()
       if a[0] == sta and a[1] == net and a[2] == cha:
          tr[i].stats['stla'] = float(a[9])
          tr[i].stats['stlo'] = float(a[10])
          tr[i].stats['evla'] = float(a[11])
          tr[i].stats['evlo'] = float(a[12])
          tr[i].stats['dist'] = float(a[13])
          tr[i].stats['gcarc']= float(a[14])
          tr[i].stats['az']   = float(a[15])
          tr[i].stats['baz']  = float(a[16])

       
    log.close()

    return tr



def makeSummary(level,tr,args):

    #define summary file names:
    log1 = "summary1.log"
    log2 = "summary2.log"
    log3 = "summary3.log"


    # open summary_1.log file
    if level==1:
       out_file = open(args.outdir + os.sep + log1,"w")
       out_file.write("H000 SUMMARY OPTIONS\n")
       out_file.write("H001 ---------------\n")
       out_file.write('H002 Begin Time        ' + args.beg + '\n')
       out_file.write('H003 Begin End         ' + args.end + '\n')
       out_file.write('H004 Station list      ' + args.sta + '\n')
       out_file.write('H005 Channel list      ' + args.cha + '\n')
       out_file.write('H006 Network list      ' + args.net + '\n')
       out_file.write('H007 Location list     ' + args.loc + '\n')
       serv = str(args.server) 
       out_file.write('H008 Server list       ' + str(args.server) + '\n')
       out_file.write('H009 Local fseed file  ' + args.fsfile + '\n')
       out_file.write('H010 Area mode         ' + args.mode + '\n')
       if args.mode == "circular":
         out_file.write('H011 center            ' + args.center + '\n')
         out_file.write('H012 radius            ' + args.radius + '\n')
       else:
         out_file.write('H011 supCor[lat lon]   ' + args.supCor + '\n')
         out_file.write('H012 infCor[lat lon]   ' + args.infCor + '\n')
       out_file.write('H013 Rotation          ' + args.rot + '\n')
       out_file.write('H014 Response          ' + args.res + '\n')
       out_file.write('H015 Format            ' + args.format + '\n')
       out_file.write('H016 OutDir            ' + args.outdir + '\n')
       out_file.write('H017 Redo              ' + 'unused' + '\n')
       out_file.write('H018 Remove gaps       ' + args.rmgaps + '\n')
       out_file.write('H019 Min Gap           ' + args.mingap + '\n')
       out_file.write('H020 Max Gap           ' + args.maxgap + '\n')
       out_file.write('H021 Reject            ' + str(args.reject) + '\n')
       out_file.write('H022 Remove mean/trt   ' + args.demean + '\n')
       out_file.write('H023 Bandpass          ' + args.bandpass + '\n')
       out_file.write('H024 Lowpass           ' + str(args.lowpass) + '\n')
       out_file.write('H025 Highpass          ' + str(args.highpass) + '\n')
       out_file.write('H026 Write filtered    ' + args.wfiltr + '\n')
       out_file.write('H027 Decimation        ' + str(args.deci) + '\n')
       out_file.write('H028 Deconvolution     ' + args.deco + '\n')
       out_file.write('H029 Sta/Lta and pick  ' + str(args.slta) + '\n')
       out_file.write('H030 PGMs              ' + args.pgm + '\n')
       out_file.write('H031 Plot Mode         ' + str(args.pltmode) + '\n')
       out_file.write('H032 Plot Channel      ' + args.pltchan + '\n')
       out_file.write('H033 Plot Component    ' + 'unused' + '\n')
       out_file.write('H034 Plot Horizontals  ' + args.pltNERT + '\n')
       out_file.write('H035 Plot Azimuth      ' + args.pltazi + '\n')
       out_file.close()

    elif level==2:
       out_file = open(args.outdir + os.sep + log2,"w")
       for i in range(len(tr)):
           if tr[i].stats['location'] == "":
              tr[i].stats['location'] = "--"

           out_file.write('%-6s' % (tr[i].stats['station']))
           out_file.write('%-3s' % (tr[i].stats['network']))
           out_file.write('%-4s' % (tr[i].stats['channel']))
           out_file.write('%-3s' % (tr[i].stats['location']))
           out_file.write('%-30s' % (tr[i].stats['starttime']))
           out_file.write('%-30s' % (tr[i].stats['endtime']))
           out_file.write('%-9.2f' % (tr[i].stats['sampling_rate']))
           out_file.write('%-6.4f' % (tr[i].stats['delta']))
           out_file.write('%12s ' % (str(tr[i].stats['npts'])))
           out_file.write('%-8.3f' % (tr[i].stats['stla']))
           out_file.write('%-8.3f' % (tr[i].stats['stlo']))
           out_file.write('%-8.3f' % (tr[i].stats['evla']))
           out_file.write('%-8.3f' % (tr[i].stats['evlo']))
           out_file.write('%-8.3f' % (tr[i].stats['dist']))
           out_file.write('%-8.3f' % (tr[i].stats['gcarc']))
           out_file.write('%-8.3f' % (tr[i].stats['az']))
           out_file.write('%-8.3f' % (tr[i].stats['baz']))
           out_file.write('\n')
       out_file.close()
            
    elif level==3:
       out_file = open(args.outdir + os.sep + log3,"w")
       out_file.write('%-6s' % "CODE")
       out_file.write('%-6s' % "Net")
       out_file.write('%-6s' % "chan")
       out_file.write('%-6s' % "loc")
       out_file.write('%8s' % "stlat")
       out_file.write('%8s' % "stlon")
       out_file.write('%8s' % "evlat")
       out_file.write('%8s' % "evlon")
       out_file.write('%10s' % "dist [km]")
       out_file.write('%8s' % "Azimuth")
       if args.pgm == "Y":
         out_file.write('%18s' % "Max Dis [m]")
         out_file.write('%18s' % "Max Vel [m/s]")
         out_file.write('%18s' % "Max Acc [m/s^2]")
         #arrange [Tsa]
         s=tr[0].stats['Tsa']
         out_file.write('%16s' % " Psa [sec]|[m/s^2]:")
         for n in range(len(s)):
           out_file.write('%10s' % (s[n]))
       if args.cfreq == "Y":
         out_file.write('%15s' % "Cfreq [Hz]")
       out_file.write('%8s' % "Sta")
       out_file.write('%8s' % "Lta")
       out_file.write('%8s' % "t_on")
       out_file.write('%8s' % "t_off")
       out_file.write('%8s' % "picks")
       out_file.write('\n')
       for i in range(len(tr)):
           out_file.write('%-6s' % (tr[i].stats['station']))
           out_file.write('%-6s' % (tr[i].stats['network']))
           out_file.write('%-6s' % (tr[i].stats['channel']))
           out_file.write('%-6s' % (tr[i].stats['location']))
           out_file.write('%8.3f' % (tr[i].stats['stla']))
           out_file.write('%8.3f' % (tr[i].stats['stlo']))
           out_file.write('%8.3f' % (tr[i].stats['evla']))
           out_file.write('%8.3f' % (tr[i].stats['evlo']))
           out_file.write('%10.1f' % (tr[i].stats['dist']))
           out_file.write('%8.3f' % (tr[i].stats['az']))
           if args.pgm == "Y":
              out_file.write('%18.3e' % (tr[i].stats['max_dis']))
              out_file.write('%18.3e' % (tr[i].stats['max_vel']))
              out_file.write('%18.3e' % (tr[i].stats['max_acc']))
              P=tr[i].stats['Gas']
              out_file.write('%19s' % " ")
              for k in range(len(P)):
                out_file.write('%10s' % (P[k]))
           if args.cfreq == "Y":
              out_file.write('%15.3e' % (tr[i].stats['cFreq']))
           out_file.write('%8.2f' % (tr[i].stats['Sta']))
           out_file.write('%8.2f' % (tr[i].stats['Lta']))
           out_file.write('%8.2f' % (tr[i].stats['trigger_on']))
           out_file.write('%8.2f' % (tr[i].stats['trigger_off']))
           out_file.write('  ')
           out_file.write('%-s' % str((tr[i].stats['picks'])))
           out_file.write('\n')
       out_file.close()


    else:
      pass  

def syncStat(cf,tr):

    # syncronize stats between two streams
    for i in range(len(tr)):
      
        tr[i].stats['Sta']=cf[i].stats['Sta']
        tr[i].stats['Lta']=cf[i].stats['Lta']
        tr[i].stats['trigger_on']=cf[i].stats['trigger_on']
        tr[i].stats['trigger_off']=cf[i].stats['trigger_off']
        tr[i].stats['picks']=cf[i].stats['picks']

    return tr
def initStats(tr):

    for i in range(len(tr)):
        tr[i].stats['max_dis']=0
        tr[i].stats['max_vel']=0
        tr[i].stats['max_acc']=0
        tr[i].stats['cFreq']=-1
        tr[i].stats['Sta']=-1
        tr[i].stats['Lta']=-1
        tr[i].stats['trigger_on']=-1
        tr[i].stats['trigger_off']=-1
        tr[i].stats['picks']=-1

    return tr

def createKML(tr,outpath):
    
    kmlDoc = minidom.Document()
    kmlElement = kmlmodule.createKMLElement(kmlDoc)
    documentElement = kmlmodule.createDocumentElement(kmlDoc)
    documentElement = kmlElement.appendChild(documentElement)    


    list_stations=[1]

    for i in range(len(tr)):

      if i==1:
        placemarkElement = kmlmodule.createPlacemarkElement(kmlDoc,  "",  "Earthquake", "")
        lat = tr[i].stats['evla']
        lon = tr[i].stats['evlo']
        ele = 0
        coordinates = [[lon,lat,ele]]
        pointElement = kmlmodule.createPointElement(kmlDoc,  "",  0,  "", coordinates )
        placemarkElement.appendChild(pointElement)
        documentElement.appendChild(placemarkElement)

        list_stations.append("EVENT")

        
      if list_stations[-1] != tr[i].stats['station']:

        placemarkElement = kmlmodule.createPlacemarkElement(kmlDoc,  "",  tr[i].stats['station'], "" )
 
   # 4) create KML <Point>
   # coordinates is a list of lists [lon, lat, elev]
        lat = tr[i].stats['stla']
        lon = tr[i].stats['stlo']
        ele = 0
        coordinates = [[lon,lat,ele]]
        pointElement = kmlmodule.createPointElement(kmlDoc,  "",  0,  "", coordinates )
        placemarkElement.appendChild(pointElement)
        documentElement.appendChild(placemarkElement)

        list_stations.append(tr[i].stats['station'])


    kmlFile = open(outpath + os.sep + 'stations.kml',  'w')
    kmlFile.write(kmlDoc.toprettyxml(' '))
    kmlFile.close()





def get_PGMs(tr,args):

   ta=Stream()
   ta=tr.copy()
   ts=tr.copy()


   for i in range(len(ta)):

      m_dis=0
      m_vel=0
      m_acc=0


      #### Displacement
      if abs(max(ta[i])) >= abs(min(ta[i])):
         m_dis=abs(max(ta[i]))
      else:
         m_dis=abs(min(ta[i]))
         
      #### Velocity
      ta[i].data = np.gradient(ta[i].data,ta[i].stats['delta'])
      if abs(max(ta[i])) >= abs(min(ta[i])):
         m_vel=abs(max(ta[i]))
      else:
         m_vel=abs(min(ta[i]))
      ts[i].data = ta[i].data
      
      #### Acceleration
      ta[i].data = np.gradient(ta[i].data,ta[i].stats['delta'])
      if abs(max(ta[i])) >= abs(min(ta[i])):
         m_acc=abs(max(ta[i]))
      else:
         m_acc=abs(min(ta[i]))

      #store obtained pgms
      tr[i].stats['max_dis']  = m_dis
      tr[i].stats['max_vel']  = m_vel
      tr[i].stats['max_acc']  = m_acc

   #define vectrors for Hz, T and G
   sa=args.sa.split(' ')
   spa=[]
   for l in range(len(sa)-1):
        spa.append(0)
   per=[]
   for l in range(len(sa)-1):
        per.append(0)
   ges=[]
   for l in range(len(sa)-1):
        ges.append(0)


   #now for each value of sa convolve with response of pendulum
   for j in range(len(sa)):
      #apply convolution
      if j >= 1:
           tu=ta.copy()
           T=eval(sa[j])*1.0
           D=eval(sa[0])
           Ts = '%5.3f' % (1/T)
           omega = (2 *  3.14159 * T)**2

           paz_sa=cornFreq2Paz(T,damp=D)
           paz_sa['sensitivity'] =omega 
           paz_sa['zeros'] = [] 
           for n in range(len(tu)):
              tu[n].simulate(paz_remove=None,paz_simulate=paz_sa,taper=True, simulate_sensitivity=True, taper_fraction=0.050000000000000003)
           
           
           per[j-1] = Ts
           
 #         #now measure for each i
           for i in range(len(tu)):
              if abs(max(tu[i])) >= abs(min(tu[i])):
                val=abs(max(tu[i]))
              else:
                val=abs(min(tu[i]))

              g=val/9.80665*100
              g='%10.3e' % (g)
              val='%10.3e' % (val)
              #here give spectral acceleration in standard units m/s^2
              # and not in g (suitable only for shakemap, can be
              # later converted
              tr[i]=UpdatePsaHeader(tr[i],j,val)

            
   for i in range(len(tr)):
     tr[i].stats['Tsa'] = per
     
   return tr



def UpdatePsaHeader(self,j,val):

    Gas = []
    if j==1:
       Gas = [val]
       self.stats['Gas'] = Gas
    else:
       Gas = self.stats['Gas']
       Gas.append(val)
       self.stats['Gas'] = Gas


    return self

def trig(self,slta):

    #get values for sta and lta
    tas = slta.split(' ')
    ON = eval(tas[2])
    OFF = eval(tas[3])


    for i in range(len(self)):
        pic = triggerOnset(self[i].data, ON, OFF)
        ooo = str()
        for j in range(len(pic)):
            ooo = ooo + str(pic[j]) 
        self[i].stats['trigger_on']  = ON
        self[i].stats['trigger_off'] = OFF
        self[i].stats['picks'] = ooo

    return self


def StaLta(self, slta):

    #get values for sta and lta
    tas = slta.split(' ')
    sta = eval(tas[0])
    lta = eval(tas[1])

    #first copy data stream. copy.data will be cft
    self_cft=self.copy()

    # for each trace of self_cft stream apply Sta/Lta
    # add sta lta values into the header
    for i in range(len(self_cft)):
        cft = recSTALTA(self_cft[i].data, \
              int(sta * self_cft[i].stats.sampling_rate), \
              int(lta * self_cft[i].stats.sampling_rate))

        # substitution data-->cft
        self_cft[i].data=cft

        # add sta lta values into the header
        self_cft[i].stats['Sta'] = sta
        self_cft[i].stats['Lta'] = lta


    return self_cft


def cFreqStream(tr):

    for i in range(len(tr)):
      
        fs=1/tr[i].stats['delta']
        cf=cfrequency(tr[i].data,fs,2,1)
        tr[i].stats['cFreq'] = cf

    return tr
        

def decimateStream(self, factor):

    c=int(factor)
    for i in range(len(self)):
       self[i].decimate(c,strict_length=False, no_filter=True)
    
    return self
     

def removeMeanTrend(tr):

    for i in range(len(tr)):
       #remove mean
       tr[i].data=tr[i].data - tr[i].data.mean()
       #remove trend
       tr[i].data=detrend(tr[i].data)

    return tr
    

def join_NERT(a,b):

    new=Stream()

    for i in range(len(a)):
        if a[i].stats['station'] == b[i].stats['station'] and \
           a[i].stats['channel'] == b[i].stats['channel']:
           new.append(a[i])
        else:
           new.append(a[i])
           new.append(b[i])
    
    return new


def rotateToGCP(self):

    tr=self.copy()

    #begin loop over data stream
    for i in range(len(tr)-1):
      # split channel
      li0 = list(tr[i+0].stats['channel'])
      li1 = list(tr[i+1].stats['channel'])

      # chech if station and part 1 of channel is identical and location
      if li0[0] == li1[0] and li0[1] == li1[1] \
         and tr[i+0].stats['station']  == tr[i+1].stats['station']\
         and tr[i+0].stats['location'] == tr[i+1].stats['location']:

         rch = li0[0] + li0[1] + 'R'
         tch = li0[0] + li0[1] + 'T'

         

         # if yes 3 possibility: EN, NE , pass
         if li0[2]=="E" and li1[2]=="N":
            #baz
            baz = tr[i].stats['baz']
            if tr[i+0].stats['npts'] == tr[i+1].stats['npts']:
               # rotate 0-1
               (tr[i+1].data,tr[i+0].data) = rotate_NE_RT(tr[i+1].data,tr[i+0].data,baz)
               tr[i+0].stats['channel']=tch
               tr[i+1].stats['channel']=rch
               i=i+1
            else:
               print "Can't rotate ",tr[i+0].stats['station'],tr[i+0].stats['channel'], " and ", \
                      tr[i+1].stats['station'],tr[i+1].stats['channel'] 

         elif li0[2]=="N" and li1[2]=="E":
            #baz
            baz = tr[i].stats['baz']
            if tr[i+0].stats['npts'] == tr[i+1].stats['npts']:
#              # rotate 1-0
               (tr[i+0].data,tr[i+1].data) = rotate_NE_RT(tr[i+0].data,tr[i+1].baz)
               tr[i+1].stats['channel']=tch
               tr[i+0].stats['channel']=rch
               i=i+1
            else:
               print "Can't rotate ",tr[i+0].stats['station'],tr[i+0].stats['channel'], " and ", \
                      tr[i+1].stats['station'],tr[i+1].stats['channel'] 

         else:
            pass 

    return tr
    

def FilterData(tr,bdp,hip,lop):

    if hip != "0":
       elements = hip.split(' ')
       cors = int(elements[0])
       freq = eval(elements[1])
       for i in range(len(tr)):
          tr[i].filter("highpass", freq=freq, corners=cors, zerophase="True")
    elif lop != "0":
       elements = lop.split(' ')
       cors = int(elements[0])
       freq = eval(elements[1])
       #print lop,elements,cors,freq
       for i in range(len(tr)):
          tr[i].filter("lowpass", freq=freq, corners=cors, zerophase="True")
    else:
       elements = bdp.split(' ')
       cors = int(elements[0])
       frem = eval(elements[1])
       freM = eval(elements[2])
       for i in range(len(tr)):
          tr[i].filter("bandpass", freqmin=frem, freqmax=freM, corners=cors, zerophase="True")

    return tr

def dlaz(lat_a,lon_a,lat_b,lon_b):

  d2r =  0.017453293    #degree-to-radians
  r2d = 57.295779515    #radians-to-degree
  deg2km = 6371 * d2r  #degree-to-kilometers
                        #this assumes the average Earth radius to be 6371 km

  #use geocentric latitude instead of geographic latitude
  #to calculate distance-aximuth-backazimuth

  #eccentricity e2:
  e2 = .0066943800      #Geodetic Reference System'80 GRS-80

  #since args are often mixed
  try:
    lat_a=eval(lat_a)
  except:
    pass
  try:
    lat_b=eval(lat_b)
  except:
    pass
  try:
    lon_a=eval(lon_a)
  except:
    pass
  try:
    lon_b=eval(lon_b)
  except:
    pass

  if lon_a > 360:
     lon_a -= 360
  if lon_b > 360:
     lon_b -= 360
  if lon_a < 0:
     lon_a += 360
  if lon_b < 0:
     lon_b += 360


  #convert from geograpic to geocentric latitude:
  lat_a_r = lat_a * d2r
  lat_b_r = lat_b * d2r
  lat_a_r_geoc = np.arctan2 ( (1-e2)*sin(lat_a_r)/cos(lat_a_r),1 )
  lat_b_r_geoc = np.arctan2 ( (1-e2)*sin(lat_b_r)/cos(lat_b_r),1 )
  lat_a = lat_a_r_geoc * r2d  #now geocentric latitude!
  lat_b = lat_b_r_geoc * r2d  #now geocentric latitude!

  #colatitude = 90 - latitude!
  colat_a = 90 - lat_a
  colat_b = 90 - lat_b

  colat_a_r = colat_a * d2r
  lon_a_r = lon_a * d2r
  colat_b_r = colat_b * d2r
  lon_b_r = lon_b * d2r

  #calculate the distance:
  #
  tmp = cos(colat_a_r)*cos(colat_b_r) + \
        sin(colat_a_r)*sin(colat_b_r)*cos(lon_b_r-lon_a_r)
  #acos_rad = np.arctan2(y, x)
  acos_rad = np.arctan2(sqrt(1-tmp*tmp),tmp)
  distance_r = acos_rad
  distance = distance_r * r2d
  distance_km = distance * deg2km

  # azimuth
  tmp = cos(colat_b_r)*sin(colat_a_r) - sin(colat_b_r)*cos(colat_a_r)*cos(lon_b_r-lon_a_r);
  tmp = tmp/sin(distance_r);
  acos_rad = np.arctan2(sqrt(1-tmp*tmp),tmp)
  az  = acos_rad * r2d
  tmp_2 = sin(colat_b_r)*sin(lon_b_r-lon_a_r)/sin(distance_r)
  if tmp_2 < 0:
      az = 360 - az

  # backazimut
  tmp = cos(colat_a_r)*sin(colat_b_r) - sin(colat_a_r)*cos(colat_b_r)*cos(lon_a_r-lon_b_r)
  tmp = tmp/sin(distance_r);
  acos_rad = np.arctan2(sqrt(1-tmp*tmp),tmp)
  baz = acos_rad * r2d
  tmp_2 = sin(colat_a_r)*sin(lon_a_r-lon_b_r)/sin(distance_r)
  if tmp_2 < 0:
      baz = 360 - baz

  
# print (">>> ",lat_a,lon_a,lat_b,lon_b,"   ",distance,az,baz,distance_km)

  return (distance,az,baz,distance_km)


def removeShortTraces(st,tolerance,Tb,Te):

    expected = Te - Tb

    noGap  = []
    yesGap = []
    nrGap  = []

    for i in range(len(st)):
        loc  = st[i].stats['location']
        staz  = st[i].stats['station']
        comp  = st[i].stats['channel']
        npts  = st[i].stats['npts']
        delta = st[i].stats['delta']
        length = npts * delta
        obtained   = length * 100 / expected
  
        if obtained <= tolerance:
           yesGap.append(st[i])
           nrGap.append(i)
        else:
           noGap.append(st[i])

    return noGap

    

def list2servers(list,redo):
  
    b=[0,0,0,0,0]
    
    if redo == "Y":
       b=[0,0,0,0,0]
    else:
       list=list.split(' ')
       if list[0] == "*":
           b=[1,1,1,1]
       else:
         for i in range(len(list)):
           if list[i] == "EIDA":
             b[0]=1 
         for i in range(len(list)):
           if list[i] == "IRIS":
             b[1]=1 
         for i in range(len(list)):
           if list[i] == "LOCAL":
             b[2]=1 
         for i in range(len(list)):
           if list[i] == "WEBDC":
             b[3]=1 
         for i in range(len(list)):
           if list[i] == "GEOPHON":
             b[4]=1 
     
    return b

def reformatChaStaList(list,target):

    if target=="eida":
       list=list.replace('*','.')
       list = list.replace(' ', '|')
    elif target=="iris":
       list=list.replace('.','*')
       list = list.replace('|', ' ')

    return list

def reformatNetStaList(list,target):

    if target=="eida":
       if   list == "*":
            list = "."
       else:
             list = list.replace(' ', '|')
    elif target=="iris":
       if   list == ".":
            list = "*"
       else:
             list = list.replace('|', ' ')

    return list

def getBBox(Sup,Inf):

    S = Sup.split(' ')
    I = Inf.split(' ')
    la=[eval(S[0]),eval(I[0])]
    lo=[eval(S[1]),eval(I[1])]
    la.sort()
    lo.sort()

    return(la[0],lo[0],la[1],lo[1])


def getXmlTagData(string):
    dom = parseString(string)
    xmlTag = dom.getElementsByTagName('Lat')[0].toxml()
    xmlLat=xmlTag.replace('<Lat>','').replace('</Lat>','')

    xmlTag = dom.getElementsByTagName('Lon')[0].toxml()
    xmlLon=xmlTag.replace('<Lon>','').replace('</Lon>','')

    xmlTag = dom.getElementsByTagName('Elevation')[0].toxml()
    xmlElevation=xmlTag.replace('<Elevation>','').replace('</Elevation>','')

    return (xmlLat,xmlLon)

def updateSacHeader(sac,dir,latStaz,lonStaz,evla,evlo):

    # load sac trace, update headers, write and close
    tr = SacIO(dir + os.sep + sac)
    tr.SetHvalue('evla',evla)
    tr.SetHvalue('evlo',evlo)
    tr.SetHvalue('stla',latStaz)
    tr.SetHvalue('stlo',lonStaz)
    (distD,Az,Baz,distkm)=dlaz(evla,evlo,latStaz,lonStaz)
    tr.SetHvalue('dist',distkm)
    tr.SetHvalue('gcarc',distD)
    tr.SetHvalue('baz',Baz)
    tr.SetHvalue('az',Az)
    tr.WriteSacHeader(dir + os.sep + sac)

    return 1

def sac4sac(self):

    out = self.split("\n")
    i=0
    new=""
    for i in range(1,len(out)):
      d=out[i].split(' ')
      if d[0] != "*":
          new=new + out[i] + "\n"

    return new

def removeInstrument(self,args):

    f = args.flim.split()
    f0 = eval(f[0])
    f1 = eval(f[1])
    f2 = eval(f[2])
    f3 = eval(f[3])


    for i in range(len(self)):
        istr = {'gain': self[i].stats.paz['gain'],
                'poles': self[i].stats.paz['poles'],
                'sensitivity': self[i].stats.paz['sensitivity'],
                'zeros': self[i].stats.paz['zeros']}
        self[i].simulate(paz_remove=istr, zero_mean=True, taper=True, taper_fraction=0.050000000000000003,pre_filt=(f0,f1,f2,f3))

    return self

def addPazStats(st, dir, sfiles): 

   # loop over sac files to find stations
   for i in range(len(st)):

          sta = st[i].stats['station']
          cha = st[i].stats['channel']
          net = st[i].stats['network']
          filename = 'SAC.PZs.' + net + '.' + sta + '.' + cha
          new = dir + os.sep + filename
          # here an empty file results into erroro
          # test if file is empty before
          try:
           if os.stat(new)[6] > 3:  
             # now test if Constant is there
             for line in open(new):
                 if "CONSTANT" in line:
                    attach_paz(st[i],new)
           else:
             print "Empty Paz file ",new
          except: 
             print "file ",new," not found"

   return st

def PzFileFromStat(st,args):
 
    for i in range(len(st)):

         sta = st[i].stats['station']
         cha = st[i].stats['channel']
         net = st[i].stats['network']
         filename = 'SAC.PZs.' + net + '.' + sta + '.' + cha 
         const = float(st[i].stats.paz.sensitivity)*float(st[i].stats.paz.gain)
         f = open(args.outdir + os.sep + filename,'w')
         
         f.write("ZEROS%4d\n" % (len((st[i].stats.paz.zeros))))
         for k in range(len(st[i].stats.paz.zeros)):
             re = st[i].stats.paz.zeros[k].real
             im = st[i].stats.paz.zeros[k].imag
             f.write("%21.6e%16.6e\n" % (re,im))
         f.write("POLES%4d\n" % (len((st[i].stats.paz.poles))))
         for k in range(len(st[i].stats.paz.poles)):
             re = st[i].stats.paz.poles[k].real
             im = st[i].stats.paz.poles[k].imag
             f.write("%21.6e%16.6e\n" % (re,im))
         f.write("CONSTANT         %12.6e" % (const))

         f.close()


def purgeListStation(st,args,ty):

    new=Stream()
    ra=args.radius.split()
    lii = []

    # select for distances
    if(ty=='d'):
      for i in range(len(st)):
          if(st[i].stats.gcarc >= eval(ra[0]) and st[i].stats.gcarc <= eval(ra[1])):
            new.append(st[i])

    return new



def updateStats(st, dir, sfile, evla, evlo): 

   # loop over sac files to find stations
   for i in range(len(st)):

          staz = st[i].stats['station']

          #loop over line of rdseed.stations
          file = open(dir + os.sep + sfile)
          for line in file:
             a = line.split(' ')
             if len(a)>=3:
              station = a[0]
              network = a[1]
              latStaz = eval(a[2])
              # check if latdepth joined
              lonStaz = eval(a[3][:6])
              # if stations are the same, upadte header and exit this loop
              if station == staz:
  
                st[i].stats['evla']=evla 
                st[i].stats['evlo']=evlo 
                st[i].stats['stla']=latStaz 
                st[i].stats['stlo']=lonStaz 
                #distkm=dlaz(evla,evlo,latStaz,lonStaz)
                (distD,Az,Baz,distkm)=dlaz(evla,evlo,latStaz,lonStaz)
                st[i].stats['dist']=distkm
                st[i].stats['gcarc']=distD
                st[i].stats['baz']=Baz
                st[i].stats['az']=Az
                break
                 
   return st

def updateSacHeaderEida(sacFiles, sourceFileFormat, outFileFormat, dir,evla,evlo): 

   # this operation works only if the source seed file is a fseed
   if sourceFileFormat == "FSEED" and outFileFormat == "SAC":

      # open rdseed.station file
#     file = open(dir + "/rdseed.stations")


      # loop over sac files to find stations
      for sac in sacFiles:

          info = sac.split('.')
          staz = info[0]

          #loop over line of rdseed.stations
          file = open(dir + os.sep + "rdseed.stations")
          for line in file:
             a = line.split(' ')
             station = a[0]
             network = a[1]
             latStaz = eval(a[2])
             lonStaz = eval(a[3])
             # if stations are the same, upadte header and exit this loop
             if station == staz:
  
                # load sac trace, update headers, write and close
                tr = SacIO(dir + os.sep + sac)            
                tr.SetHvalue('evla',evla)
                tr.SetHvalue('evlo',evlo)
                tr.SetHvalue('stla',latStaz)
                tr.SetHvalue('stlo',lonStaz)
                (distD,Az,Baz,distkm)=dlaz(evla,evlo,latStaz,lonStaz)
                tr.SetHvalue('dist',distkm)
                tr.SetHvalue('gcarc',distD)
                tr.SetHvalue('baz',Baz)
                tr.SetHvalue('az',Az)
                #distkm=dlaz(evla,evlo,latStaz,lonStaz)
                tr.WriteSacHeader(dir + os.sep + sac)
                break
                 
   return sacFiles


def findResponseFiles(dir,mode):

   # scan teh directory dir, find RESP files and PAZ files
   # depending on the mode number (1,2,3), seed function extractResponse
   # for details
   allFiles=os.listdir(dir)
 
   # go through dir and select files wich start with RESP andor SAC_PAZ
   allNames = []
   for i in range(len(allFiles)):
     paz =allFiles[i].split('_')
     if paz[0] == "SAC" and paz[1] == "PZs":
        newname = paz[0] + "." + paz[1] + "." +\
                  paz[2] + "." + paz[3] + "." +\
                  paz[4]
        source = dir + os.sep + allFiles[i]
        destin = dir + os.sep + newname
        allNames.append(newname)
        cmd_move = "mv %s %s" %(source,destin)
              
        os.system(cmd_move)

   #print allNames

   return (1,allNames)
    

def extractResponse(seedFile,extractMode,outDir):

    # Call rdseed and extract station file, Respo and PAZ file
    # - seedFile must be a full seed
    # - extractMode = 0 --> nothoing to do (this func not called) 
    #                 1 --> RESP    
    #                 2 --> PAZ 
    #                 3 --> RESP and PAZ 
    
    # set method
    if extractMode == "1":
       cmd_rdseed = "rdseed  -f %s -S -R -q %s" %(seedFile,outDir)
    elif extractMode == "2":
       cmd_rdseed = "rdseed  -f %s -S -p -q %s" %(seedFile,outDir)
    elif extractMode == "3":
       cmd_rdseed = "rdseed  -f %s -S -R -p -q %s" %(seedFile,outDir)
    else:
       cmd_rdseed = "rdseed  -f %s -S -q %s" %(seedFile,outDir)
    
    # extract
    try: 
       os.system(cmd_rdseed)
    except:
       print seedFile, ": No useful seed file to explode"

    # load resp and paz file names
    (respofiles,pazfiles) = findResponseFiles(outDir,extractMode)
    
    return(respofiles,pazfiles)


def grabIngvEidaArchive(self,format):
  
    #define root after extraction
    rootName = self.split('.')
    archivename = rootName[0].split(os.sep)
    #archive file name
    FileName = rootName[0] + os.sep + archivename[-1] + "." + format 
    subprocess.call(['tar', '-C', os.sep + "tmp", '-xf', self])

    return rootName[0],FileName



def fromFseed2sac(self,newFormat,outpath,ending):
    
   out = []
   for i in range(len(self)):
     sta = self[i].stats['station']
     com = self[i].stats['channel']
     net = self[i].stats['network']
     beT = self[i].stats['starttime']
     enT = self[i].stats['endtime']
     Loc = self[i].stats['location']
     StartTime = self[i].stats['starttime']
     BeginTime = UTCDateTime(StartTime)
     Year        = "%04d"%(BeginTime.year)
     Month       = "%02d"%(BeginTime.month)
     Day         = "%02d"%(BeginTime.day)
     hour        = "%02d"%(BeginTime.hour)
     minute      = "%02d"%(BeginTime.minute)
     second      = "%02d"%(BeginTime.second)
     microsecond = "%06d"%(BeginTime.microsecond)

     if ending == "slt":
        ending = 'stalta.SAC'

     sacname = str(sta) + "." + str(Loc) + "." + str(com) + "." + str(net) + "." + \
               str(Year) + str(Month) + str(Day) + "_" + \
               str(hour) + str(minute) + str(second) + "." + \
               str(microsecond) + "." + ending

     self[i].write(outpath + os.sep + sacname, format = newFormat)
     out.append(sacname) 

   return out


def removeGaps(self, min_gap, max_gap, verbose="False"): 

    """
    Returns the Stream object without trace gaps/overlaps.
    :param min_gap: All gaps smaller than this value will be omitted. The
          value is assumed to be in seconds. Defaults to None.
    :param max_gap: All gaps larger than this value will be omitted. The
          value is assumed to be in seconds. Defaults to None.
    :param verbose: stdout traces removed. Default verbose=False
    """

    new=Stream()
    self.sort()
    gap_list = []

    # since one would be left
    if(len(self) != 0):
      self.append(self[0])

    for _i in xrange(1,len(self.traces) - 0):
       # skip traces with different network, station, location or channel
       if self.traces[_i - 1].id != self.traces[_i + 0].id:
          new.append(self.traces[_i])
          continue
       # different sampling rates should always result in a gap or overlap
       if self.traces[_i - 1].stats.delta == self.traces[_i + 0].stats.delta:
          flag = True
       else:
          flag = False
       stats = self.traces[_i - 1].stats
       stime = stats['endtime']
       etime = self.traces[_i + 0].stats['starttime']
       delta = etime.timestamp - stime.timestamp

       # Check that any overlap is not larger than the trace coverage
       if delta < 0:
             temp = self.traces[_i + 0].stats['endtime'].timestamp - \
                    etime.timestamp
             if (delta * -1) > temp:
                 delta = -1 * temp
       # Check gap/overlap criteria
       if min_gap and delta < min_gap:
             new.append(self.traces[_i - 1])
             continue
       if max_gap and delta > max_gap:
             new.append(self.traces[_i - 1])
             continue
       # Number of missing samples
       nsamples = int(round(fabs(delta) * stats['sampling_rate']))
       # skip if is equal to delta (1 / sampling rate)
       if flag and nsamples == 1:
             new.append(self.traces[_i - 1])
             continue
       elif delta > 0:
             nsamples -= 1
       else:
             nsamples += 1

       gap_list.append([_i,stats['network'], stats['station'],
                             stats['location'], stats['channel'],
                             stime, etime, delta, nsamples])
       if verbose == "True" or verbose == "TRUE" or verbose == "true":
          print  "Removed because of gap: ",stats['network'],stats['station'],stats['channel'],stime,etime,delta, nsamples

    return new

def mkdir(newdir):

    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """

    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)
