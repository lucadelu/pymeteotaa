#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:55:00 2017

@author: lucadelu
"""

PROPERTIES = {
    'air-temperature': {'unit': '°C',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature'},
    'air-relative-humidity': {'unit': '%',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:humidity:relative'},
    'air-rainfall': {'unit': 'mm',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall'},
    'air-wind-velocity': {'unit': 'm/s',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity'},
    'air-wind-direction': {'unit': '°',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:direction'},
    'air-wind-gust': {'unit': 'm/s',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:gust'},
    'air-pressure': {'unit': 'hPa',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:pressure'},
    'solar-radiation-time': {'unit': 's',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:solar:radiation:time'},
    'solar-radiation': {'unit': 'W/m²',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:solar:radiation'},
    'snow-height': {'unit': 'cm',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:snow:height'},
    'river-height': {'unit': 'cm',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:river:water:height'},
    'river-flowrate': {'unit': 'm³/s',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:river:water:flowrate'},
    'river-temperature': {'unit': '°C',
     'istsos': 'urn:ogc:def:parameter:x-istsos:1.0:meteo:water:temperature'}
}

PROPERTIES_ST = {
    'LT': 'air-temperature',
    'LF': 'air-relative-humidity',
    'N': 'air-rainfall',
    'WG': 'air-wind-velocity',
    'WR': 'air-wind-direction',
    'WG.BOE': 'air-wind-gust',
    'LD.RED': 'air-pressure',
    'SD': 'solar-radiation-time',
    'GS': 'solar-radiation',
    'HS': 'snow-height',
    'W': 'river-height',
    'Q': 'river-flowrate',
    'WT': 'river-temperature',
#    'SSTF':
}

PROPERTIES_PAT = {
    'temperature_list': ['air-temperature'],
    'relative_humidity_list': ['air-relative-humidity'],
    'precipitation_list' : ['air-rainfall'],
    'wind_list': ['air-wind-velocity', 'air-wind-direction'],
    'global_radiation_list': ['solar-radiation'],
    'snow_depth_list': ['snow-height']
}


def istsos_sep(val):
    """Return values for the new registercsv.py script

    :param str val: the istsos observation string
    """
    cats = val.split('1.0:')[1].split(':')
    return cats[0], cats[1], ':'.join(cats[2:])


class ObsProperties:
    """Class for manage observed properties"""
    def __init__(self, code=None, desc_de=None, desc_it=None, desc_l=None,
                 unit=None, name=None, istsos=None):
        self._sensor_code = code
        self._sensor_de = desc_de
        self._sensor_it = desc_it
        self._sensor_l = desc_l
        self._unit = unit
        self._istsos = istsos
        self._name = name

    def get_code(self):
        """Class to get observation property code"""
        return self._sensor_code

    def set_code(self, value):
        """Class to set observation property code"""
        self._sensor_code = value

    def del_code(self):
        """Class to delete observation property code"""
        del self._sensor_code

    sensor_code = property(get_code, set_code, del_code, "The South Tyrol" \
                           "observation property code")

    def get_de(self):
        """Class to get German description"""
        return self._sensor_de

    def set_de(self, value):
        """Class to set German description"""
        self._sensor_de = value

    def del_de(self):
        """Class to delete German description"""
        del self._sensor_de

    sensor_de = property(get_de, set_de, del_de, "The German description")

    def get_it(self):
        """Class to get Italian description"""
        return self._sensor_it

    def set_it(self, value):
        """Class to set Italian description"""
        self._sensor_it = value

    def del_it(self):
        """Class to delete Italian description"""
        del self._sensor_it

    sensor_it = property(get_it, set_it, del_it, "The Italian description")

    def get_l(self):
        """Class to get Ladin description"""
        return self._sensor_l

    def set_l(self, value):
        """Class to set Ladin description"""
        self._sensor_l = value

    def del_l(self):
        """Class to delete Ladin description"""
        del self._sensor_l

    sensor_l = property(get_l, set_l, del_l, "The Ladin description")

    def get_unit(self):
        """Class to get the used unit"""
        return self._unit

    def set_unit(self, value):
        """Class to set the used unit"""
        self._unit = value

    def del_unit(self):
        """Class to delete the used unit"""
        del self._unit

    unit = property(get_unit, set_unit, del_unit, "The used unit")

    def get_name(self):
        """Class to get the used name"""
        return self._name

    def set_name(self, value):
        """Class to set the used name"""
        self._unit = value

    def del_name(self):
        """Class to delete the used name"""
        del self._unit

    name = property(get_name, set_name, del_name, "The name")

    def get_istsos(self):
        """Class to get istSOS definition"""
        return self._istsos

    def set_istsos(self, value):
        """Class to set istSOS definition"""
        self._istsos = value

    def del_istsos(self):
        """Class to delete istSOS definition"""
        del self._istsos

    istsos = property(get_istsos, set_istsos, del_istsos, "The istSOS definition")
