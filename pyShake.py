#!/usr/bin/env python -W ignore::DeprecationWarning
# encoding: utf-8

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from obspy.core import read
import sys,os

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def getSTationslist(self):

    list=[]
    n=0

    for i in range(len(self)):
       list.append(self[i].stats['station'])

    # to be shure are really ordered
    list.sort()

    # list of distances
    out  = []
    for i in range(len(self)-1):
       if(self[i].stats['station'] != self[i+1].stats['station']):
          out.append(self[i].stats['station'])
    out.append(self[-1].stats['station'])

    return (out)

def defheader():

   header = '<?xml version="1.0" encoding="US-ASCII" standalone="yes"?>\n' + \
            '<!DOCTYPE stationlist [\n' + \
            '<!ELEMENT stationlist (station)+>\n' + \
            '<!ATTLIST stationlist created CDATA #REQUIRED>\n' + \
            '<!ELEMENT station (comp)+>\n' + \
            '<!ATTLIST station code CDATA #REQUIRED>\n' + \
            '<!ATTLIST station name CDATA #REQUIRED>\n' + \
            '<!ATTLIST station insttype CDATA #REQUIRED>\n' + \
            '<!ATTLIST station lat CDATA #REQUIRED>\n' + \
            '<!ATTLIST station lon CDATA #REQUIRED>\n' + \
            '<!ATTLIST station source (SCSN | CGS | NSMP) "SCSN">\n' + \
            '<!ATTLIST station commtype (DIG | ANA) "DIG">\n' + \
            '<!ATTLIST station dist CDATA "10.0">\n' + \
            '<!ATTLIST station loc CDATA "">\n' + \
            '<!ELEMENT comp (acc , vel , psa*)>\n' + \
            '<!ATTLIST comp name CDATA #REQUIRED>\n' + \
            '<!ATTLIST comp originalname CDATA #IMPLIED>\n' + \
            '<!ELEMENT acc EMPTY>\n' + \
            '<!ELEMENT vel EMPTY>\n' + \
            '<!ELEMENT psa03 EMPTY>\n' + \
            '<!ELEMENT psa10 EMPTY>\n' + \
            '<!ELEMENT psa30 EMPTY>\n' + \
            '<!ATTLIST acc value CDATA #REQUIRED>\n' + \
            '<!ATTLIST acc flag CDATA "">\n' + \
            '<!ATTLIST vel value CDATA #REQUIRED>\n' + \
            '<!ATTLIST vel flag CDATA "">\n' + \
            '<!ATTLIST psa03 value CDATA #REQUIRED>\n' + \
            '<!ATTLIST psa03 flag CDATA "">\n' + \
            '<!ATTLIST psa10 value CDATA #REQUIRED>\n' + \
            '<!ATTLIST psa10 flag CDATA "">\n' + \
            '<!ATTLIST psa30 value CDATA #REQUIRED>\n' + \
            '<!ATTLIST psa30 flag CDATA "">\n' + \
            ']>' 

   return header


def getXMLInfoStation(tr):
    
    ST = tr.stats.station
    NT = tr.stats.network
    LAT = str(tr.stats.stla)
    LON = str(tr.stats.stlo)
    out = '  <station insttype=\"\" source=\"\" code=\"' + ST + '\" name=\"\"' + \
          ' netid=\"' + NT + '\" lat="' + LAT + '" lon="' + LON + '" commtype=\"\">'

    return out
  
def getXMLInfoChannel(tr):
    
    li = []
    CH = str(tr.stats.channel)
    acc = str(tr.stats.max_acc/9.80665*100)
    vel = str(tr.stats.max_vel*100)
    sa  = tr.stats.Gas
    psa03 = str(float(sa[0])/9.80665*100)
    psa10 = str(float(sa[1])/9.80665*100) 
    psa30 = str(float(sa[2])/9.80665*100)
    li1   = '    <comp name="' + CH + '">'
    li2   = '      <acc value="' + acc + '"/>'
    li3   = '      <vel value="' + vel + '"/>'
    li4   = '      <psa03 value="' + psa03 + '"/>'
    li5   = '      <psa10 value="' + psa10 + '"/>'
    li6   = '      <psa30 value="' + psa30 + '"/>'
    li7   = '    </comp>'
    li.append(li1)
    li.append(li2)
    li.append(li3)
    li.append(li4)
    li.append(li5)
    li.append(li6)
    li.append(li7)

    return li
  

def export4ShakeMap(data):

    # definitions
    top = defheader()
    lines = []
    begStationList = '<stationlist created=\"\">' 
    endStation = '  </station>'
    endStationList = '</stationlist>'
    checkStation = 0
    checkChannel = 0

    # get list of stations
    stationList = getSTationslist(data)

    # Begin adding lines to lines
    lines.append(begStationList)

    for j in range(len(stationList)):
      for i in range(len(data)):

        if(data[i].stats.station == stationList[j]):
        
           if(checkStation==0):
             infoStation = getXMLInfoStation(data[i])
             lines.append(infoStation)
             checkStation = 1
           
           infoChannel = getXMLInfoChannel(data[i])
           for k in range(len(infoChannel)):
               lines.append(infoChannel[k])

        if(data[i].stats.station != stationList[j] and checkStation == 1):
           checkStation = 0
           lines.append(endStation)
          
    lines.append(endStation)
    lines.append(endStationList)

    return (top,lines)

def writeShake(top,lines,args):

    try:
        f = open(args.outdir + os.sep + args.pgmfile,"w")
        try:
           f.write(top) # Write a string to a file
           for i in range(len(lines)):
              f.write(lines[i] + '\n') # Write a string to a file
        finally:
           f.close()
    except IOError:
        pass
   

