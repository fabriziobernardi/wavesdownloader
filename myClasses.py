from copy import deepcopy, copy
from obspy.core.utcdatetime import UTCDateTime
from obspy.core.util import AttribDict, createEmptyDataChunk, deprecated, \
                            interceptDict
import numpy as np
import math
import warnings


class Stats(AttribDict):

 def __init__(self, header={}):
        """
        """
        # set default values without calculating derived entries
        super(Stats, self).__setitem__('evdp',-1)
        super(Stats, self).__setitem__('evla',-1)
        super(Stats, self).__setitem__('evlo',-1)
        super(Stats, self).__setitem__('stla',-1)
        super(Stats, self).__setitem__('stlo',-1)
        super(Stats, self).__setitem__('stel',-1)
#       # set default values for all other headers
#       header.setdefault('calib', 1.0)
#       for default in ['station', 'network', 'location', 'channel']:
#           header.setdefault(default, '')
#       # initialize
#       super(Stats, self).__init__(header)
#       # calculate derived values
#       self._calculateDerivedValues()

class SacIO(object):

      def fromarray(self, trace, begin=0.0, delta=1.0, distkm=0,
                  starttime=UTCDateTime("1970-01-01T00:00:00.000000")):
        """
        Create a SAC file from an numpy.ndarray instance

        >>> t = SacIO()
        >>> b = np.arange(10)
        >>> t.fromarray(b)
        >>> t.GetHvalue('npts')
        10
        """
        if not isinstance(trace, np.ndarray):
            raise SacError("input needs to be of instance numpy.ndarray")
        else:
            # Only copy the data if they are not of the required type
            self.seis = np.require(trace, '<f4')
        # convert stattime to sac reference time, if it is not default
        if begin == -12345:
            reftime = starttime
        else:
            reftime = starttime - begin
        # if there are any micro-seconds, use begin to store them
        millisecond = reftime.microsecond // 1000                # integer arithmetic
        microsecond = (reftime.microsecond - millisecond * 1000) # integer arithmetic
        if microsecond != 0:
            begin += microsecond * 1e-6
        # set a few values that are required to create a valid SAC-file
        self.SetHvalue('int1', 2)
        self.SetHvalue('cmpaz', 0)
        self.SetHvalue('cmpinc', 0)
        self.SetHvalue('nvhdr', 6)
        self.SetHvalue('leven', 1)
        self.SetHvalue('lpspol', 1)
        self.SetHvalue('lcalda', 0)
        self.SetHvalue('nzyear', reftime.year)
        self.SetHvalue('nzjday', reftime.strftime("%j"))
        self.SetHvalue('nzhour', reftime.hour)
        self.SetHvalue('nzmin', reftime.minute)
        self.SetHvalue('nzsec', reftime.second)
        self.SetHvalue('nzmsec', millisecond)
        self.SetHvalue('kcmpnm', 'Z')
        self.SetHvalue('svla', 0)
        self.SetHvalue('svlo', 0)
        self.SetHvalue('evla', 0)
        self.SetHvalue('evlo', 0)
        self.SetHvalue('iftype', 1)
        self.SetHvalue('npts', len(trace))
        self.SetHvalue('delta', delta)
        self.SetHvalue('b', begin)
        self.SetHvalue('e', begin + (len(trace) - 1) * delta)
        self.SetHvalue('iztype', 9)
        self.SetHvalue('dist', distkm)

