#!/usr/bin/env python
# encoding: utf-8


"""
Classes pertaining to events - using the database architecture

Created by Alessia Maggi and Alberto Michelini.
"""
import os
from EidaSpeaker import *

class INGV_requestor(object):
  """
  Deals with INGV web services.
  """

  def __init__(self,username,password,data_dir='/tmp',db_worker=None, db=None):
    self.username=username
    self.password=password
   # self.ws_script=os.getenv('WEB_SERVICES')+os.sep+'ingv_ws_data_client.jar'
    self.data_dir=data_dir
    self.db_worker=db_worker
    self.db=db
    self.ws_time_format="%Y-%m-%dT%H:%M:%S"
    self.st_time_format="%Y,%j,%H:%M:%S.%f"


  def run_circular_query(self,Net,Staz,Chan,lat,lon,min_radius,max_radius,start_time,end_time,file_type):


      Speak= EidaSpeaker(self.username,self.password)

      try : 
         self.data_name=Speak.dataRequestCircular(Net,Staz,Chan,".",start_time,end_time,min_radius,\
 		"%s %s"%(lat,lon),max_radius,"%s %s"%(lat,lon),self.data_dir + os.sep ,file_type)
#		"%s %s"%(lat,lon),max_radius,"%s %s"%(lat,lon),self.data_dir + "/",file_type)
      except RequestError,e : 
         print e

      return (self.data_dir,self.data_name)

  
  def run_rectangular_query(self,Net,Staz,Chan,latDown,lonDown,latUp,lonUp,start_time,end_time,file_type):

      Speak= EidaSpeaker(self.username,self.password)

      try : 
          self.data_name=Speak.dataRequestRect(Net,Staz,Chan,".",start_time,end_time,\
               "%s %s"%(latDown,lonDown),"%s %s"%(latUp,lonUp),self.data_dir + os.sep,file_type)
      except RequestError,e : 
         print e

      return (self.data_dir,self.data_name)


