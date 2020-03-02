#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:55:37 2017

@author: lucadelu
"""
import os
import sys
import requests
import geojson
import tempfile
from lxml import etree
from .observed_properties import ObsProperties
from .observed_properties import PROPERTIES
from .observed_properties import PROPERTIES_ST
from .observed_properties import PROPERTIES_PAT
from .observed_properties import istsos_sep
from .observations import Observations_ST
from .observations import Observations

LANGUAGES = {'E': 'English', 'D': 'German', 'I': 'Italian', 'L': 'Ladin'}
STATION_ST = {'MS': {'I': 'Stazione Meteo', 'DE': 'Wetterstation',
                     'E': 'Weather Station'},
              'WS': {'I': 'Stazione Vento in Quota', 'DE': 'Höhenwindstation'},
              'SF': {'I': 'Stazione Neve', 'DE': 'Schneemessfeld'},
              'PG': {'I': 'Stazione Idrometrica', 'DE': 'Pegelstation'}}
DATA_ISTSOS = "urn:ogc:def:parameter:x-istsos:1.0:time:iso8601"
PAT_STATIONS = "http://dati.meteotrentino.it/service.asmx/getListOfMeteoStations"

class Station(object):
    """Class to define a station"""
    def __init__(self, code=None, name_de=None, name_it=None, name_l=None,
                 name_en=None, alt=None, long=None, lat=None):
        self._code = code
        self._name_de = name_de
        self._name_it = name_it
        self._name_l = name_l
        self._name_en = name_en
        self._altitude = alt
        self._longitude = long
        self._latitude = lat
        self._geom = None
        self.observer_properties = {}
        self.observations = {}
        self.last_observations = {}

    def get_code(self):
        """Get the station code"""
        return self._code

    def set_code(self, value):
        """Set the station code"""
        self._code = value

    def del_code(self):
        """Delete the station code"""
        del self._code

    code = property(get_code, set_code, del_code,
                    "The station's South Tyrol code")

    def get_de(self):
        return self._name_de

    def set_de(self, value):
        self._name_de = value

    def del_de(self):
        del self._name_de

    name_de = property(get_de, set_de, del_de, "The station's German name")

    def get_it(self):
        return self._name_it

    def set_it(self, value):
        self._name_it = value

    def del_it(self):
        del self._name_it

    name_it = property(get_it, set_it, del_it, "The station's Italian name")

    def get_l(self):
        return self._name_l

    def set_l(self, value):
        self._name_l = value

    def del_l(self):
        del self._name_l

    name_l = property(get_l, set_l, del_l, "The station's Ladin name")

    def get_en(self):
        return self._name_en

    def set_en(self, value):
        self._name_en = value

    def del_en(self):
        del self._name_en

    name_en = property(get_en, set_en, del_en, "The station's English name")

    def get_alt(self):
        return self._altitude

    def set_alt(self, value):
        self._altitude = value

    def del_alt(self):
        del self._altitude

    altitude = property(get_alt, set_alt, del_alt, "The station's altitude")

    def get_long(self):
        return self._longitude

    def set_long(self, value):
        self._longitude = value

    def del_long(self):
        del self._longitude

    longitude = property(get_long, set_long, del_long,
                         "The station's longitude")

    def get_lat(self):
        return self._latitude

    def set_lat(self, value):
        self._latitude = value

    def del_lat(self):
        del self._latitude

    latitude = property(get_lat, set_lat, del_lat, "The station's latitude")

    def get_geom(self):
        return self._geom

    def set_geom(self):
        self._geom = geojson.Point((self.get_long(), self.get_lat()))

    def del_geom(self):
        del self._geom

    geom = property(get_geom, set_geom, del_geom, "GeoJSON geometry")

    def _check_dates(self):
        """Check if dates are the same, and return the differences"""
        prev = []
        check = {}
        out = True
        outdates = None
        if self.observations:
            for key, obss in self.observations.items():
                dates = obss.get_dates()
                check[key] = {len(dates): dates}
                if not prev:
                    prev = (len(dates), dates)
                    outdates = dates
                else:
                    if len(dates) != prev[0]:
                        out=False
                        #print(list(set(prev[1]) - set(dates)), list(set(dates) - set(prev[1])))
                        if len(dates) > prev[0]:
                            outdates = dates
        return out, outdates


    def get_name(self, lang):
        if lang == 'D':
            return self.get_de()
        elif lang == 'I':
            return self.get_it()
        elif lang == 'L':
            return self.get_l()
        elif lang == 'E':
            return self.get_en()
        else:
            print('ERROR: language not supported')

    def obs_istsos_output(self, output=True, path=None):
        """Write the observations to a CSV file

        :param str output: output file to write otherwise it print to stdout
        """
        if output:
            if path:
                out = open(path, 'w')
            else:
                out = open(os.path.join(tempfile.gettempdir(),
                                        "{na}.csv".format(na=self.get_code())),
                           'w')
        else:
            out = sys.stdout
        obsprops = tuple(self.observer_properties.keys())
        head = "{da}".format(da=DATA_ISTSOS)
        for prop in obsprops:
            head += ",{it}".format(it=self.observer_properties[prop].istsos)
        out.write("{he}\n".format(he=head))
        datescheck, dates = self._check_dates()
        if datescheck:
            print("")
        for dat in dates:
            row = "{da}".format(da=dat)
            for key, obs in self.observations.items():
                row += ",{vl}".format(vl=obs.get_observation(dat))
            out.write("{he}\n".format(he=row))
        if output:
            print(out.name)
            out.close()


class Station_ST(Station):
    """Class to define a South Tyrol station

    The attributes for each station are
    - SCOPE: station's id
    - NAME_D: German name
    - NAME_I: Italian name
    - NAME_L: Ladin name
    - NAME_E: English name
    - ALT: altitude AMSL
    - LONG: longitude
    - LAT: latitude
    """
    def __init__(self, code=None, name_de=None, name_it=None, name_l=None,
                 name_en=None, alt=None, long=None, lat=None):
        super(Station_ST, self).__init__()
        self._code = code
        self._name_de = name_de
        self._name_it = name_it
        self._name_l = name_l
        self._name_en = name_en
        self._altitude = alt
        self._longitude = long
        self._latitude = lat

    def get_observed_props(self):
        """Get the observed property for this station"""
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors?" \
              "station_code={st}".format(st=self.get_code())
        myreq = requests.get(url)
        myjson = myreq.json()
        for feat in myjson:
            prop = PROPERTIES_ST[feat['TYPE']]
            obs = ObsProperties(code=feat['TYPE'], desc_de=feat['DESC_D'],
                                desc_it=feat['DESC_I'], desc_l=feat['DESC_L'],
                                istsos=PROPERTIES[prop]['istsos'],
                                unit=PROPERTIES[prop]['unit'],
                                name=prop)
            self.observer_properties[prop] = obs

    def get_last_values(self):
        """Get the last values for this station"""
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors?" \
              "station_code={st}".format(st=self.get_code())
        myreq = requests.get(url)
        myjson = myreq.json()
        for feat in myjson:
            prop = PROPERTIES_ST[feat['TYPE']]
            self.last_observations[prop] = {feat['DATE']: feat['VALUE']}

    def get_observations(self, prop=None, lastdate=None, startdate='20140801'):
        """Get all the observations

        :param str prop: the choosen property, if None it will use all the
                         properties of the station
        :param str lastdate: the last date to query in format YYYYMMDD, if None
                             it will use today
        :param str startdate: the first date to query in format YYYYMMDD, the
                              first date available is 2014-08-01
        """
        if isinstance(prop, str):
            props = [prop]
        elif isinstance(prop, list):
            props = prop
        else:
            if len(self.observer_properties.keys()) == 0:
                self.get_observed_props()
            props = self.observer_properties.keys()
        for pr in props:
            obs = Observations_ST(self.observer_properties[pr])
            obs.get_values(self.get_code(), lastdate, startdate)
            self.observations[pr] = obs


class Station_PAT(Station):
    """Class to define a Trentino Province station

    The attributes for each station are
    """
    def __init__(self, code=None, name_it=None, name_en=None, alt=None,
                 long=None, lat=None, start=None, end=None):
        super(Station_PAT, self).__init__()
        self._code = code
        self._name_de = name_it
        self._name_it = name_it
        self._name_l = name_it
        self._name_en = name_en
        self._altitude = alt
        self._longitude = long
        self._latitude = lat
        self._startdate = start
        self._enddate = end
        self.url_data = "http://dati.meteotrentino.it/service.asmx/getLast" \
                        "DataOfMeteoStation?codice={st}"

    def get_start(self):
        return self._startdate

    def set_start(self, value):
        self._startdate = value

    def del_start(self):
        del self._startdate

    startdate = property(get_start, set_start, del_start,
                         "The station's start date")

    def get_end(self):
        return self._enddate

    def set_end(self, value):
        self._enddate = value

    def del_end(self):
        del self._enddate

    enddate = property(get_end, set_end, del_end, "The station's end date")

    def get_info(self):
        """Get the info for the station"""
        myreq = requests.get(PAT_STATIONS)
        stazioni = etree.fromstring(myreq.content)
        for stazione in stazioni:
            infos = {}
            for child in stazione.getchildren():
                key = child.tag.replace('{http://www.meteotrentino.it/}','')
                infos[key] = child.text
            if infos['code'] == self._code:
                self.startdate = infos['startdate']
                self.enddate = infos['enddate']
                self.latitude = float(infos['latitude'])
                self.longitude = float(infos['longitude'])
                self.altitude = float(infos['elevation'])
                self.name_it = infos['name']
                self.name_en = infos['shortname']
                self.name_de = infos['name']
                self.name_l = infos['name']
                self.set_geom()
                self.get_observed_props()
                break

    def get_observed_props(self):
        """Get the observed property for this station"""
        url = self.url_data.format(st=self.get_code())
        myreq = requests.get(url)
        vals = etree.fromstring(myreq.content)
        for feat in vals.getchildren():
            key = feat.tag.replace('{http://www.meteotrentino.it/}','')
            if len(feat.getchildren()) > 0:
                props = PROPERTIES_PAT[key]
                for prop in props:
                    obs = ObsProperties(code=key, name=prop,
                                        istsos=PROPERTIES[prop]['istsos'],
                                        unit=PROPERTIES[prop]['unit'])
                    self.observer_properties[prop] = obs

    def get_last_values(self):
        """Get the last values for this station"""
        url = self.url_data.format(st=self.get_code())
        myreq = requests.get(url)
        allvals = etree.fromstring(myreq.content)
        for feat in allvals.getchildren():
            key = feat.tag.replace('{http://www.meteotrentino.it/}','')
            if len(feat.getchildren()) > 0:
                props = PROPERTIES_PAT[key]
                ele = feat.getchildren()[-1]
                vals = ele.getchildren()
                if key == 'wind_list':
                    for prop in props:
                        if prop == 'air-wind-velocity':
                            self.last_observations[prop] = {vals[0].text: vals[1].text}
                        elif prop == 'air-wind-direction':
                            self.last_observations[prop] = {vals[0].text: vals[2].text}
                else:
                    self.last_observations[props[0]] = {vals[0].text: vals[1].text}

    def get_observations(self, prop=None):
        """Get values for the last 24 hours

        :param str prop: the choosen property, if None it will use all the
                         properties of the station
        """
        if isinstance(prop, str):
            props = [prop]
        elif isinstance(prop, list):
            props = prop
        else:
            if len(self.observer_properties.keys()) == 0:
                self.get_observed_props()
            props = self.observer_properties.keys()
        url = self.url_data.format(st=self.get_code())
        myreq = requests.get(url)
        allvals = etree.fromstring(myreq.content)
        for feat in allvals.getchildren():
            key = feat.tag.replace('{http://www.meteotrentino.it/}','')
            vals = feat.getchildren()
            if len(vals) > 0:
                props = PROPERTIES_PAT[key]
                if key == 'wind_list':
                    wvel = Observations(self.observer_properties['air-wind-velocity'])
                    wdir = Observations(self.observer_properties['air-wind-direction'])
                    for val in vals:
                        wvel.add_observation(val[0].text, val[1].text)
                        wdir.add_observation(val[0].text, val[2].text)
                    self.observations['air-wind-velocity'] = wvel
                    self.observations['air-wind-direction'] = wdir
                else:
                    obs = Observations(self.observer_properties[props[0]])
                    for val in vals:
                        obs.add_observation(val[0].text, val[1].text)
                    self.observations[props[0]] = obs


class MeteoStations:
    """This class is used to download the data of weather stations

    :param int epsg: the output coordinate system in EPSG code, it works only
                     with GeoJSON output format
    :param str oformat: the output format, CSV or JSON (this return a GeoJSON)
    """
    def __init__(self, epsg=4326, oformat='JSON'):
        """Function for the initialize the object"""
        self.epsg = epsg
        self.format = oformat
        self.req = None
        self.stations_list = []

    def get_stations_ST(self):
        """Return a list of code and name of South Tyrol stations"""
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/stations"
        myreq = requests.get(url)
        myjson = myreq.json()
        for feat in myjson['features']:
            st = Station_ST(code=feat['properties']['SCODE'],
                            name_de=feat['properties']['NAME_D'],
                            name_it=feat['properties']['NAME_I'],
                            name_l=feat['properties']['NAME_L'],
                            name_en=feat['properties']['NAME_E'],
                            alt=feat['properties']['ALT'],
                            long=feat['properties']['LONG'],
                            lat=feat['properties']['LAT'])
            st.set_geom()
            st.get_observed_props()
            self.stations_list.append(st)

    def get_stations_PAT(self):
        """Return a list of code and name of Trento Province stations"""
        myreq = requests.get(PAT_STATIONS)
        stazioni = etree.fromstring(myreq.content)
        for stazione in stazioni:
            st = Station_PAT()
            for child in stazione.getchildren():
                key = child.tag.replace('{http://www.meteotrentino.it/}','')
                if key == 'code':
                    st.code = child.text
                elif key == 'name':
                    st.name_de = child.text
                    st.name_it = child.text
                    st.name_l = child.text
                elif key == 'shortname':
                    st.name_en = child.text
                elif key == 'elevation':
                    st.altitude = float(child.text)
                elif key == 'latitude':
                    st.latitude = float(child.text)
                elif key == 'longitude':
                    st.longitude = float(child.text)
                elif key == 'startdate':
                    st.startdate = child.text
                elif key == 'enddate':
                    st.enddate = child.text
            st.set_geom()
            st.get_observed_props()
            self.stations_list.append(st)

    def get_stations(self):
        """Set the stations"""
        self.get_stations_PAT()
        self.get_stations_ST()

    def print_codes_names(self, lang='E'):
        """Return a list of code and name of stations

        :param str lang: a letter rappresenting the language for the name
                         (supported values are: E - English, D - German,
                          I - Italian, L - Ladin)
        """
        if lang not in LANGUAGES.keys():
            print('ERROR: language not supported')
            sys.exit(1)
        if len(self.stations_list) == 0:
            self.get_stations()
        for st in self.stations_list:
            print(st.get_code(), st.get_name(lang))

    def out_stations_istsos(self, output=None, lang='E', alls=True):
        """Write the station information to a CSV file to be imported with
        registercsv.py

        :param str output: output file to write otherwise it print to stdout
        :param str lang: the language name

        This script register new procedures importing data from a csv file
        containing the followings columns:

        1.  name
        2.  description
        3.  keyword
        4.  long name
        5.  modelNumber
        6.  manufacturer
        7.  sensorType
        8.  foi-epsg
        9.  foi-coordinates (x,y,z comma separated for more then one)
        10. foi-name
        11. observed property (comma separated for more then one)
        12. uom (comma separated for more then one)
        13. begin position
        14. end position
        15. resolution
        16. acquisition interval
        17. quality index - lower bound
        18. quality index - upper bound


        separated with a semicolumn symbol ";"
        """
        if output:
            out = open(output,'w')
        else:
            out = sys.stdout
        for st in self.stations_list:
            if not alls and len(st.observer_properties.items()) == 0:
                continue
            myfoi = "{na}_{co}".format(na=st.get_name(lang).replace(' ','_'),
                                       co=st.get_code())
            infos = "{co};{de};;;;;;{ep};{ex},{ey},{ez};" \
                    "{foi}".format(co=st.get_code(), foi=myfoi, ep=self.epsg,
                                   ex=st.longitude, ey=st.latitude,
                                   de=myfoi.replace('_', ' '),
                                   ez=st.altitude)
            typ = []
            cats = []
            props = []
            uoms = []
            for key, pro in st.observer_properties.items():
                vals = istsos_sep(pro.istsos)
                typ.append(vals[0])
                cats.append(vals[1])
                props.append(vals[2])
                uoms.append(pro.unit)
            out.write("{inf};{ty};{cs};{ps};{us}".format(inf=infos,
                                                         ty=','.join(typ),
                                                         cs=','.join(cats),
                                                         ps=','.join(props),
                                                         us=','.join(uoms)))
            out.write(";;;;;-;-;\n")
        if output:
            out.close()

    def out_stations(self, output=None, lang='E', alls=True):
        """Write the station information to a CSV file without observation
        properties

        :param str output: output file to write otherwise it print to stdout
        :param str lang: the language name
        """
        if output:
            out = open(output,'w')
        else:
            out = sys.stdout
        for st in self.stations_list:
            if len(st.observer_properties.items()) != 0:
                continue
            myfoi = "{na}_{co}".format(na=st.get_name(lang).replace(' ','_'),
                                       co=st.get_code())
            infos = "{co};{foi};{ep};{ex};{ey};{ez}".format(co=st.get_code(),
                                                            foi=myfoi,
                                                            ep=self.epsg,
                                                            ex=st.longitude,
                                                            ey=st.latitude,
                                                            ez=st.altitude)
            if hasattr(st, 'startdate'):
                infos += ";{sd}".format(sd=st.startdate)
            if hasattr(st, 'enddate'):
                infos += ";{ed}".format(ed=st.enddate)

            out.write("{inf}\n".format(inf=infos))
        if output:
            out.close()

    def get_observations(self, props=None):
        """Get observations for each stations

        :param props: it could e string or a list containing names
                      of properties
        """
        for st in self.stations_list:
            if len(st.observer_properties.items()) == 0:
                continue
            st.get_observations(props)
        return True

    def out_observations_istsos(self, output=True, path=None):
        """Write the observations to a CSV file to be imported with

        :param str output: write otherwise print to stdout
        :param str path: output file to write otherwise it save in temporary
                         directory with station code
        """
        for st in self.stations_list:
            if len(st.observer_properties.items()) == 0:
                continue
            st.obs_istsos_output(output, path)
        return True

    def out_geojson(self, output=None, lang='E', onlyobs=False):
        """Write the station in GeoJSON format to a file or stdout

        :param str output: output file to write otherwise it print to stdout
        :param str lang: the language name
        """
        if output:
            out = open(output,'w')
        else:
            out = sys.stdout
        feats = []
        for st in self.stations_list:
            if not onlyobs and len(st.observer_properties.items()) == 0:
                continue
            obs = []
            for key, pro in st.observer_properties.items():
                obs.append(key)
            poi = geojson.Point((st.longitude, st.latitude))
            if st.startdate:
                dat = st.startdate
            else:
                dat = None
            feat = geojson.Feature(geometry=poi,
                                   properties={"code": st.get_code(),
                                               "place": st.get_name(lang),
                                               "properties": obs,
                                               "start_date": dat})
            feats.append(feat)

        jsonfeats = geojson.FeatureCollection(feats)
        out.write(geojson.dumps(jsonfeats, sort_keys=True))
        if output:
            out.close()
