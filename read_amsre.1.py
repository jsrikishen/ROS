import os
import socket

import numpy as np
from netCDF4 import Dataset, num2date
from datetime import datetime


class CETB:

    def __init__(self, sensor, date, hemisphere='N'):

        self.sensor = sensor  # this variable should perhaps become platform_sensor or just platform
        self.hemisphere = hemisphere

        # Paths
        if socket.gethostname().find('gs615-caribou') >= 0:
        # path Ludo
            self.path_in = os.getenv('HOME') + '/Spaceborne/CETB/' + self.sensor + '/'
        elif socket.gethostname().find('gs615-oibserve') >= 0:
        # path server
            self.path_in = '/crevasse/Spaceborne/CETB/' + self.sensor + '/'
        elif socket.gethostname().find('discover') >= 0:
        # path Jayanthi
            self.path_in = '/gpfsm/dnb32/jsrikish/ROS/data/NSIDC-0630-'

        if self.sensor == 'AMSRE':
            self.satellite = 'AQUA'

        self.sensor = sensor

        # Convert date (yyyymmdd) to yyyyDOY
        self.year = date.strftime("%Y")[0:4]
        self.doy = '%03d' % date.timetuple().tm_yday

    def load(self, channel='all', orbit='E', interpolation_method='SIR'):

        if (len(channel)==0):
                list_channel =['18V']
        elif channel[0]== "all":
                list_channel = ['6V','6H','10V','10H','18V', '18H', '23V', '23H', '36V', '36H', '89V', '89H']
        else:
                list_channel=channel
        for channel in list_channel:
                if channel[0:1] == '6' or channel[0:2] == '10':
                        resolution = '12.5'
                if channel[0:2] == '18' or channel[0:2] == '23':
                        resolution = '6.25'
                elif channel[0:2] == '36' or channel[0:2] == '89':
                        resolution = '3.125'
                channel2 = channel[-1] + channel[0:2]
                print channel2
                channel2 = TBclass(channel2)
                filename = self.path_in + \
                         'EASE2_' + self.hemisphere + resolution + 'km-' + self.satellite + \
                        '_' + self.sensor + '-' + self.year + self.doy + '-' + channel + \
                        '-'+orbit+'-' + interpolation_method + '-RSS-v1.3.nc'

                print filename
                ncfile = Dataset(filename, "r", format="NETCDF4")
                if channel == '18V':
                        setattr(self, 'V18', channel2)
                elif channel == '18H':
                        setattr(self, 'H18', channel2)
                elif channel == '23V':
                        setattr(self, 'V23', channel2)
                elif channel == '23H':
                        setattr(self, 'H23', channel2)
                elif channel == '36V':
                        setattr(self, 'V37', channel2)
                elif channel == '36H':
                        setattr(self, 'H37', channel2)
                elif channel == '89V':
                        setattr(self, 'V89', channel2)
                elif channel == '89H':
                        setattr(self, 'H89', channel2)
                setattr(channel2, 'tb', np.squeeze(
                     ncfile.variables['TB'][:]))
                setattr(channel2, 'std', np.squeeze(
                     ncfile.variables['TB_std_dev'][:]))
                setattr(channel2, 'numsamples', np.squeeze(
                     ncfile.variables['TB_num_samples'][:]))
                ncfile.close()


class TBclass(object):

    def __init__(self,channel):
       self.channel=channel
       
if __name__ == '__main__':

    hemisphere = 'N'
    date = datetime(2002, 9, 27)
    sensor = 'AMSRE'

#   User input for channels  & orbit
#   channel=['18V','18H']
#   channel=['all']
    channel=[]
    orbit='M'
    cetb = CETB(sensor, date)

    if (len(channel)==0):
      CETB.load(cetb, channel=channel,orbit=orbit)
      print np.mean(cetb.V18.tb)
      V18_asc=cetb.V18.tb
      orbit='E'
      CETB.load(cetb, channel=channel,orbit=orbit)
      print np.mean(cetb.V18.tb)
      V18_des=cetb.V18.tb


