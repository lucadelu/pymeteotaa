#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 12:11:05 2017

@author: lucadelu
"""
import requests
from collections import OrderedDict
from datetime import datetime
from datetime import date
INPUT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%Z'
OUTPUT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

YYYYMMDD = '%Y%m%d'

class Observations():
    """Class for a single observation"""
    def __init__(self, obs_prop=None):
        self._obs_prop = obs_prop
        self.values = OrderedDict()

    def get_obsprop(self):
        """Get observation property object"""
        return self._obs_prop

    def set_obsprop(self, value):
        """Set observation property object"""
        self._obs_prop = value

    def del_obsprop(self):
        """Delete observation property"""
        del self._obs_prop

    obs_prop = property(get_obsprop, set_obsprop, del_obsprop,
                        "The observed property")

    def add_observation(self, data, value):
        """Add observation with date and value"""
        self.values[data] = value

    def get_observation(self, data):
        """Get observation from data"""
        try:
            return self.values[data]
        except KeyError:
            return ''

    def print_observations(self):
        """Print all observations"""
        for k, v in self.values.items():
            print(k, v)

    def get_dates(self):
        """Return all dates"""
        return sorted(self.values.keys())


class Observations_ST(Observations):
    """Class for a single observation"""
    def __init__(self, obs_prop=None):
        super(Observations_ST, self).__init__()
        self._obs_prop = obs_prop

    def get_values(self, station, lastdate=None, startdate='20140801'):
        """Add values from the json"""
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/timeseries?" \
              "station_code={st}&sensor_code={se}&date_from={df}&date_to={dt}"
        if not lastdate:
            lastdateobj = datetime.combine(date.today(), datetime.min.time())
        else:
            lastdateobj = datetime.strptime(lastdate, YYYYMMDD)
        startdateobj = datetime.strptime(startdate, YYYYMMDD)

        while startdateobj < lastdateobj:
            myurl = url.format(st=station, se=self.get_obsprop().sensor_code,
                               dt=lastdateobj.strftime(YYYYMMDD), df=startdate)
            myreq = requests.get(myurl)
            myjson = myreq.json()
            for val in myjson:
                self.add_observation(val['DATE'], val['VALUE'])
            dateobj = datetime.strptime(self.get_dates()[0], INPUT_TIME_FORMAT)
            if lastdateobj == dateobj:
                break
            lastdateobj = dateobj
        return
