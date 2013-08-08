#!/usr/bin/env python
# encoding: utf-8

import sys,os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from operator import itemgetter
from obspy.signal.trigger import plotTrigger
from obspy.signal.trigger import triggerOnset
from matplotlib.backends.backend_pdf import PdfPages
from myUsefullFuncs import decimateStream


def plotWaves(tr,mode,kmrad,area,chan,nert,aziplot,cft,slta,outdir,rot):

  tr=decimateStream(tr,10)
 

  if slta!="None":
    tas = slta.split(' ')
    sta = eval(tas[0])
    lta = eval(tas[1])
    thrOn=eval(tas[2])
    thrOff=eval(tas[3])
  else:
    thrOn=0
    thrOff=0


  if len(tr) == 0:
     print "No traces to plot"
     sys.exit() 
    
  # normalization to (kmrad[1]-kmrad[0])/len(tr)   
  if(rot == "Y"):
     normlization=(kmrad[1]-kmrad[0]) / (float(len(tr))/2) * 6
  else:
     normlization=(kmrad[1]-kmrad[0]) / (float(len(tr))/2) * 3
     
  if mode ==2:
     for i in range(len(tr)):
         tr[i].data=(tr[i].data/max(abs(tr[i].data)))*normlization
  else:
     for i in range(len(tr)):
         tr[i].data=(tr[i].data/max(abs(tr[i].data)))

  #number of subplots
  nr_subpl = len(tr)

  #starting level for y_axe
  axe_y_lev=0
  xpoM1 = 0
  xpoM2 = 0
  xpoM3 = 0

  # create empty list
  mykmList=[None]*len(tr)

  (Amin,Amax)=aziplot.split(' ')
  Amin=eval(Amin)
  Amax=eval(Amax)


  #loop over nr_subpl
  # define figures to save
  fig1=plt.figure(1)
  if nert == "RT" or nert == "NE":
     fig2=plt.figure(2)
     fig3=plt.figure(3)
  for i in range(nr_subpl):

    # when --redo==Y: header valued of dist and az do not exist
    try:
       refaz = tr[i].stats['az']
    except:
       refaz = 0
       tr[i].stats['az']=refaz

    # define controller for plotting azimuth. This allows to plot
    # for example 20-50 or 330-20 cases
    pltAziController=0
    if mode >= 1:
       if Amin<=Amax:
          if refaz >= Amin and refaz <= Amax:
              pltAziController=1 
       else:
          if refaz <= Amin and refaz >= Amax:
             pltAziController=0
          else:
             pltAziController=1

    if pltAziController==1:

         # y-axe
         # when --redo==Y: header valued of dist and az do not exist
         try:
           dist=tr[i].stats['dist']
         except:
           dist= 10
           tr[i].stats['dist']=dist
           
         # x- axe
         tBegin = 0
         tEnd   = tr[i].stats.endtime.timestamp \
                - tr[i].stats.starttime.timestamp
         t      = np.arange(tBegin,tEnd,tr[i].stats.delta)
         nt     = len(t)
         ntr=len(tr[i].data)
         if nt == ntr:
            pass
         elif nt < ntr:
            tr[i].data=tr[i].data[:nt]
         elif ntr < nt:
            t=t[:ntr]

         # Labels and info
         xPosText = 0
         kPosText = t[len(t)-1]+0 
         distanceToPlot = "%8.2f" % (dist)
         nametoPlot     = "%-9s"   % (tr[i].stats['station'])
         li = list(tr[i].stats['channel'])
         if mode == 2:
            axe_y_lev = dist
            dista = int(tr[i].stats['dist'])
            azimu = int(tr[i].stats['az'])
            textdist = r"$\Phi$ = " + `azimu` + u"\u00b0"
            xlab = "Time [s]"
            ylab = "Distance [km]"
         else:
            textdist = ""
            xlab = "Time [s]"
            ylab = "Nr Traces"

#        try:
         if slta!="None":
            onOff = np.array(triggerOnset(cft[i].data, thrOn, thrOff))
#        except IndexError:
#               pass

         df = tr[i].stats.sampling_rate

         if mode == 1:
            pik=0.5
         else:
            pik=5.0

         if li[2] == "Z" and li[0] == chan:
              if mode == 1:
                 axe_y_lev = xpoM1
              plt.figure(1)
              plt.plot(t,tr[i].data+axe_y_lev,color='k')
              plt.text(xPosText, axe_y_lev, tr[i].stats['station'],fontsize=10,backgroundcolor='#99FFFF') #99FFFF
              plt.text(kPosText, axe_y_lev,textdist ,fontsize=8, backgroundcolor='#F0FFFF')
              plt.xlabel(xlab)
              plt.ylabel(ylab)
              plt.title(tr[i].stats['channel'])
              i=axe_y_lev-pik
              j=axe_y_lev+pik
              if slta!="None":
                 try:
                    plt.vlines(onOff[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
                 except IndexError:
                    pass
              xpoM1 += 1
         if nert == "RT":
           if li[2] == "T" and li[0] == chan:
              if mode == 1:
                 axe_y_lev = xpoM2
              plt.figure(2)
              plt.plot(t,tr[i].data+axe_y_lev,color='k')
              plt.text(xPosText, axe_y_lev, tr[i].stats['station'],fontsize=10,backgroundcolor='#99FFFF')
              plt.text(kPosText, axe_y_lev,textdist ,fontsize=8,backgroundcolor='#F0FFFF')
              plt.xlabel(xlab)
              plt.ylabel(ylab)
              plt.title(tr[i].stats['channel'])
              i=axe_y_lev-pik
              j=axe_y_lev+pik
              if slta!="None":
                 try:
                    plt.vlines(onOff[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
                 except IndexError:
                    pass
              xpoM2 += 1
           elif li[2] == "R" and li[0] == chan:
              if mode == 1:
                 axe_y_lev = xpoM3
              plt.figure(3)
              plt.plot(t,tr[i].data+axe_y_lev,color='k')
              plt.text(xPosText, axe_y_lev, tr[i].stats['station'],fontsize=10,backgroundcolor='#99FFFF')
              plt.text(kPosText, axe_y_lev,textdist ,fontsize=8,backgroundcolor='#F0FFFF')
              plt.xlabel(xlab)
              plt.ylabel(ylab)
              plt.title(tr[i].stats['channel'])
              i=axe_y_lev-pik
              j=axe_y_lev+pik
              if slta!="None":
                 try:
                    plt.vlines(onOff[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
                 except IndexError:
                    pass
              xpoM3 += 1
           else:
              pass
         elif nert == "NE":
           if li[2] == "N" and li[0] == chan:
              if mode == 1:
                 axe_y_lev = xpoM2
              plt.figure(2)
              plt.plot(t,tr[i].data+axe_y_lev,color='k')
              plt.text(xPosText, axe_y_lev, tr[i].stats['station'],fontsize=8,backgroundcolor='#99FFFF')
              plt.text(kPosText, axe_y_lev,textdist ,fontsize=8,backgroundcolor='#F0FFFF')
              plt.xlabel(xlab)
              plt.ylabel(ylab)
              plt.title(tr[i].stats['channel'])
              i=axe_y_lev-pik
              j=axe_y_lev+pik
              if slta!="None":
                 try:
                    plt.vlines(onOff[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
                 except IndexError:
                    pass
              xpoM2 += 1
           elif li[2] == "E" and li[0] == chan:
              if mode == 1:
                 axe_y_lev = xpoM3
              plt.figure(3)
              plt.plot(t,tr[i].data+axe_y_lev,color='k')
              plt.text(xPosText, axe_y_lev, tr[i].stats['station'],fontsize=8,backgroundcolor='#99FFFF')
              plt.text(kPosText, axe_y_lev,textdist ,fontsize=8,backgroundcolor='#F0FFFF')
              plt.xlabel(xlab)
              plt.ylabel(ylab)
              plt.title(tr[i].stats['channel'])
              i=axe_y_lev-pik
              j=axe_y_lev+pik
              if slta!="None":
                 try:
                    plt.vlines(onOff[:, 0] / df, i, j, color='r', lw=2, label="Trigger On")
                 except IndexError:
                    pass
              xpoM3 += 1
           else:
              pass

  fig1.savefig(outdir + os.sep + 'plotWavesZ.pdf')
  if nert == "NE":
     fig2.savefig(outdir + os.sep + 'plotWavesNS.pdf')
     fig3.savefig(outdir + os.sep + 'plotWavesEW.pdf')
  if nert == "RT":
     fig2.savefig(outdir + os.sep + 'plotWavesT.pdf')
     fig3.savefig(outdir + os.sep + 'plotWavesR.pdf')
  plt.show()
