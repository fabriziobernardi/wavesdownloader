from obspy.core import UTCDateTime,Stream
from obspy.arclink.client import Client
from myUsefullFuncs import dlaz
from obspy.core.util.attribdict import AttribDict
import sys,os

def getDataViaArcLink(t1,t2,inv,args):

    client = Client(user='test@obspy.org')

    data = Stream()

    a = inv.keys() 
    for i in range(len(a)):
        l = a[i].split('.')
        if len(l) <= 2:
           pass
        else:
           Net = l[0]
           Sta = l[1]
           Cha = l[3]

           try: 
             st = client.getWaveform(Net, Sta, "", Cha, UTCDateTime(t1), UTCDateTime(t2), metadata="TRUE")
             data.append(st[0])
           except:
             pass
   
    return data


def getInventoryViaArcLink(t1,t2,center,grradius,bbox,args):


    client = Client(user='test@obspy.org')

    coordLimits=getCoordLimits(center,grradius,bbox,args)


    inv = client.getInventory(args.net, '*', '*', args.cha, starttime=UTCDateTime(t1), endtime=UTCDateTime(t2), \
                             min_latitude=coordLimits[0], max_latitude=coordLimits[1], \
                             min_longitude=coordLimits[2], max_longitude=coordLimits[3])

    return inv

def getCoordLimits(center,gr,bbox,args):

    if args.mode == "rectangular":
       return [bbox[0],bbox[2],bbox[1],bbox[3]]

    elif args.mode == "circular":
       # approximation circle -> square
       minLat = float(center[0])-float(gr[1])
       maxLat = float(center[0])+float(gr[1])
       minLon = float(center[1])-float(gr[1])
       maxLon = float(center[1])+float(gr[1])
       return [minLat,maxLat,minLon,maxLon]

    else:
       return [-1,-1,-1,-1]

def writeWbDcStation(st, args):

    (evla,evlo)=args.center.split(' ')


    st_file = open(args.outdir + os.sep + 'webdc.stations','w')
    for i in range(len(st)):
        stla=st[i].stats.coordinates.latitude
        stlo=st[i].stats.coordinates.longitude
        st[i].stats.evla = eval(evla) 
        st[i].stats.evlo = eval(evlo)
        st[i].stats.stla = stla
        st[i].stats.stlo = stlo
        (distD,Az,Baz,distkm)=dlaz(evla,evlo,stla,stlo)
        st[i].stats['dist']=distkm
        st[i].stats['gcarc']=distD
        st[i].stats['baz']=Baz
        st[i].stats['az']=Az
        st_file.write("%s %s %s %s %s\n" % (st[i].stats.station, st[i].stats.network, st[i].stats.stla, st[i].stats.stlo, st[i].stats.coordinates.elevation))

    st_file.close()

    return st
