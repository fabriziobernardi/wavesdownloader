from suds.client import Client
import time
import urllib2
import sys

class EidaSpeaker :
	"""
	Could do circularRequest or Rectangular request from the URL : http://eida.rm.ingv.it
	"""
	#definition of attributs
	#the url where you can find the wsdl file
        url='http://webservices.rm.ingv.it/webservices/ingv_ws_data/wsdl/ingv_ws_data2.wsdl'
	client=Client(url)
	stationidentifier=client.factory.create('StationIdentifierFilterType')
	spabounds=client.factory.create('SpatialBoundsType')
	Crown=client.factory.create("CrownSelectionType")
	Innercircle=client.factory.create("CircleByCenterPointType")
	Outercircle=client.factory.create("CircleByCenterPointType")
	timeperiods=client.factory.create('TimePeriodType')
	temporalbounds=client.factory.create('TemporalBoundsType')
	User=client.factory.create('UserTokenType')
	envelope=client.factory.create('EnvelopeType')
	bndbox=client.factory.create('BoundingBoxType')


	#initialization
	def __init__(self,email,password):
		"""
		initialization need the email and the password of an eida account
		"""
		self.User.email=email
		self.User.password=password

	def dataRequestCircular(self,NetworkCode,StationCode,ChannelCode,LocId,Timebegin,Timeend,InnerRadius,InnerPosition,OuterRadius,OuterPosition, DataName,DataFormat='FSEED'):
		"""
		Methode to ask circular datafile at the webservice
		"""
		self.stationidentifier.NetworkCode=NetworkCode
		self.stationidentifier.StationCode=StationCode
		self.stationidentifier.ChannelCode=ChannelCode
		self.stationidentifier.LocId=LocId
		self.timeperiods.beginPosition=Timebegin
		self.timeperiods.endPosition=Timeend
		self.temporalbounds.TimePeriod=self.timeperiods
		self.stationidentifier.TimeSpan=self.temporalbounds
		self.Innercircle.pos=InnerPosition
		self.Innercircle.radius=InnerRadius
		self.Outercircle.pos=OuterPosition
		self.Outercircle.radius=OuterRadius
		self.Crown.innerCircle=self.Innercircle
		self.Crown.outerCircle=self.Outercircle
		self.spabounds.CrownSelection=self.Crown
		self.Dataname=DataName
		resultRequest=self.client.service.dataRequest(self.User,self.stationidentifier,self.spabounds,DataFormat)
                # Check if submission request miss user and passwd
                if resultRequest.StatusResponse.CodeDescription != "SUBMITTED":
                   print "-----"
                   print resultRequest.StatusResponse.CodeDescription
                   print "Exit!!"
                   print "-----"
                   sys.exit(0)

		self.ID=resultRequest.StatusResponse.RequestID.split('/')
		if resultRequest.StatusResponse.Code == -1 :
			raise RequestError(resultRequest.StatusResponse.CodeDescription+"\n")
			
		else :
			resultStatus=self.client.service.checkStatus(self.User,resultRequest.StatusResponse.RequestID)
			while resultStatus.StatusResponse.CodeDescription !="DONE" :
				resultStatus=self.client.service.checkStatus(self.User,resultRequest.StatusResponse.RequestID)
				time.sleep(1)

			#It is the url to download the files
			URLDownload=resultStatus.StatusResponse.DownloadURL
			print "URL: ",URLDownload
			#copy files from the url to the computer
			dossier= urllib2.urlopen(URLDownload).read()
			print self.Dataname+str((self.ID)[2])+"_data.tgz"
			f2=open(self.Dataname+str((self.ID)[2])+"_data.tgz", "w")
			f2.write(dossier)
			f2.close()

			#clean
			resultPurge=self.client.service.dataPurge(self.User,resultRequest.StatusResponse.RequestID)
		return str((self.ID)[2])


	def dataRequestRect(self,NetworkCode,StationCode,ChannelCode,LocId,Timebegin,Timeend,LowerCorner,UpperCorner, DataName,DataFormat='FSEED'):
		"""
		Methode to ask rectangular datafile at the webservice
		"""
		self.stationidentifier.NetworkCode=NetworkCode
		self.stationidentifier.StationCode=StationCode
		self.stationidentifier.ChannelCode=ChannelCode
		self.stationidentifier.LocId=LocId
		self.timeperiods.beginPosition=Timebegin
		self.timeperiods.endPosition=Timeend
		self.temporalbounds.TimePeriod=self.timeperiods
		self.stationidentifier.TimeSpan=self.temporalbounds
		self.envelope.lowerCorner=LowerCorner
		self.envelope.upperCorner=UpperCorner
		self.bndbox.Envelope=self.envelope
		self.spabounds.BoundingBox=self.bndbox
		self.Dataname=DataName
		resultRequest=self.client.service.dataRequest(self.User,self.stationidentifier,self.spabounds,DataFormat)
                # Check if submission request miss user and passwd
                if resultRequest.StatusResponse.CodeDescription != "SUBMITTED":
                   print "-----"
                   print resultRequest.StatusResponse.CodeDescription
                   print "Exit!!"
                   print "-----"
                   sys.exit(0)
		self.ID=resultRequest.StatusResponse.RequestID.split('/')

		if resultRequest.StatusResponse.Code == -1 :
			raise RequestError(resultRequest.StatusResponse.CodeDescription+"\n")
			
		else :
			resultStatus=self.client.service.checkStatus(self.User,resultRequest.StatusResponse.RequestID)
			while resultStatus.StatusResponse.CodeDescription !="DONE" :
				resultStatus=self.client.service.checkStatus(self.User,resultRequest.StatusResponse.RequestID)
				time.sleep(1)

			#It is the url to download the files
			URLDownload=resultStatus.StatusResponse.DownloadURL
			#copy files from the url to the computer
			dossier= urllib2.urlopen(URLDownload).read()
			print self.Dataname+str(self.ID)+"_data.tgz"
			f2=open(self.Dataname+str((self.ID)[2])+"_data.tgz", "w")
			f2.write(dossier)
			f2.close()

			#clean
			resultPurge=self.client.service.dataPurge(self.User,resultRequest.StatusResponse.RequestID)
		return str((self.ID)[2])



class RequestError(Exception):
    """
    definition of an exception classe
    """
    def __init__(self,raison):
        self.raison = raison
    
    def __str__(self):
        return self.raison
