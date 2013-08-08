#!/usr/bin/env python -W ignore::DeprecationWarning
# encoding: utf-8

################################################################
#
# Script wavesdownloader: download seismic data and metadata from archives
#
# HELP: type ./wavesdownloader (or ./wavesdownloader -h)
#
################################################################


#################################################################
# ----  A. Import classes and functions ----                    #
from myParser import checkConsistency,parseMyLine
from func_wd import wavesdownloader
import sys,os


##################################################################
# ----  B. Parse arguments ----                                  #
# and give process ID 
args=parseMyLine()
ll = sys.argv[1:]
if not ll:
       print "Use -h or --help option for Help"
       sys.exit(0)

try: 
   print "Process ID: ",os.getpid()
except:
   pass

##################################################################
# ----  C. call wavesdownloader ----                              #
wavesdownloader(args)
