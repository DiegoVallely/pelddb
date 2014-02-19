# -*- coding: utf-8 -*-

import datetime as dt
from read_data.read_data import *
from dictionaries.dictionaries import spot_dict
import os

path = os.path.abspath("applications/peld/data_samples/")


class InsertDB(object):
    """docstring for InsertDB"""
    def __init__(self, db):
        super(InsertDB, self).__init__()
        self.db = db
        

    def set_data(self):
        
        # EXAMPLE OF TIDBIT DATA INSERTION WORKFLOW
        peld_start_date = dt.date(2013, 10, 1)
        peld_end_date = dt.date(2043, 10, 1)


        tidbit = ReadTidbit(path+"/dados_tidbit_pontadacabeca_nov-09_a_set-11")


        # let's assume that institution, project and cruise were not yet inserted in the database
        # INSERTING INSTITUTION
        ieapm = self.db.institution.insert(name="IEAPM")
        # INSERTING PROJECT
        peld = self.db.project.insert(name="PELD", institution_id=ieapm)
        # INSERTING CRUISE
        rede_peld = self.db.cruise.insert(name="REDE PELD", platform_type="Estação Fixa",
                                    platform_name="Tidbit", start_date=peld_start_date,
                                    end_date=peld_end_date, institution_id=ieapm,
                                    project_id=peld)
        # INSERTING STATION
        ptcabeca = self.db.station.insert(local_sea=u"Mar de Fora", spot_name="Ponta da Cabeça",
                                    start_date=tidbit.dates[0], end_date=peld_end_date,
                                    start_time=tidbit.times[0], end_time=None, local_depth=8.,
                                    lon=-42.0381, lat=-22.9770, capture_type=u"Senso de Temperatura",
                                    cruise_id=rede_peld)
        # INSERTING OCEANOGRAPHIC PARAMETERS
        for sample in range(len(tidbit.temps)):
            s = self.db.oceanography.insert(dates=tidbit.dates[sample], times=tidbit.times[sample],
                                    depths=5., temperature=tidbit.temps[sample], station_id=ptcabeca)    

        # EXAMPLE OF BIOLOGICAL SHEET DATA INSERTION WORKFLOW
        enseada = DataSheet1(path+"/enseada.xls")
        date, spot, station, temp, salt, oxig, fosfate, nitrate, amonium, silicate, chla = enseada.get_data()

        antigos = self.db.project.insert(name="ANTIGOS", institution_id=ieapm)
        # antigos_cruise = db.cruise.insert(name="ANTIGOS", institution_id=ieapm, project_id=antigos)

        for s in range(len(spot)):
            for key, values in zip(spot_dict.keys(), spot_dict.values()):
                for item in values:
                    if item == spot[s]:
                        lon = spot_dict[key][1]
                        lat = spot_dict[key][2]

            st = self.db.station.insert(local_sea="Mar de Dentro", spot_name=spot[s],
                                    name=str(station[s]), lon=lon, lat=lat, capture_type="Biology")

            d = self.db.oceanography.insert(dates=date[s], temperature=temp[s], salt=salt[s],
                                        chla=chla[s], oxigen=oxig[s], fosfate=fosfate[s],
                                        nitrate=nitrate[s], amonium=amonium[s], silicate=silicate[s],
                                        station_id=st)