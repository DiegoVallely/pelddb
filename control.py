#! -*- coding: utf-8 -*- 
# Control database acesses and data queries.

# TODO list ==============================================================
#   Incrementar query para checar se ja existe determinado ProfileData no 
#   banco de dados
#=========================================================================

import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import array
from geoalchemy import *

from model import *

import matplotlib.pyplot as plt
import numpy as np
# from wx.lib.pubsub import setupkwargs
# from wx.lib.pubsub import pub as Publisher

import platform

class SessionManager(object):
    def __init__(self):
        if platform.system() == 'Windows':
            self.engine = create_engine('postgresql://postgres:1234@localhost:5432/peldDB', echo=False)
        else:    
            self.engine = create_engine('postgresql://:5432/peldDB', echo=False)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()


S = SessionManager()

def dbQuit():
    S.session.close()




class InsertCruise(object):
    def __init__(self, cruise):
        self.obj_profiles = []
        self.cruise = cruise
        self.metadata = []

    def get_or_create(self, S, table, **kwargs):
        """ Generic method to get some data from db, if does not exists yet, creates a new record."""
        instance = S.session.query(table).filter_by(**kwargs).first()
        
        if not instance:
            instance = table(**kwargs)
            S.session.add(instance)
            print "NEW %s instance created!" %(table)
            S.session.commit()
            self.data_exists = False
        else:
            print "Instance of %s EXISTS" %(table)
            self.data_exists = True
        return instance


    def save_cruise(self, S):  

        if self.cruise['cruise']['institution']:
            if self.cruise['cruise']['institution']['country']:
                country = self.cruise['cruise']['institution']['country']
                country_obj = self.get_or_create(S, Country, name=country)
                country_id = country_obj.id
            else:
                country_id = None
            institution = self.cruise['cruise']['institution']['name']
            institution_obj = self.get_or_create(S, Institution, name=institution,
                                                                    country=country_id)
            institution_id = institution_obj.id
        else:
            institution_id = None

        cruise = self.cruise['cruise']
        self.cruise_obj = self.get_or_create(S, Cruise, cruise_name=cruise['cruise_name'],
                                        platform_name=cruise['platform_name'],
                                        platform_type=cruise['platform_type'],
                                        institution=institution_id,
                                        start_date=cruise['start_date'],    
                                        end_date=cruise['end_date'], )
        S.session.commit()

    def save_profile(self, S, profile):
        temp_variable = dict(long_name=u'Temperature', short_name=u'temp', unit=u'C')
        salt_variable = dict(long_name=u'Salinity', short_name=u'salt', unit=u' ')
        instrument = self.cruise['instrument']

        if instrument['itype'] == 'CTD':
            temp_obj = self.get_or_create(S, Variable, long_name=temp_variable['long_name'], 
                                                  short_name=temp_variable['short_name'], 
                                                  unit=temp_variable['unit'])
            salt_obj = self.get_or_create(S, Variable, long_name=salt_variable['long_name'], 
                                                  short_name=salt_variable['short_name'], 
                                                  unit=salt_variable['unit'])
        elif instrument['itype'] == 'XBT':
            temp_obj = self.get_or_create(S, Variable, long_name=temp_variable['long_name'], 
                                                  short_name=temp_variable['short_name'], 
                                                  unit=temp_variable['unit'])
        elif instrument['itype'] == 'ARGO':
            pass
        else:
            pass

        instrument = self.cruise['instrument']
        filename = profile.filename.split('/')[-1]
        inst_obj = self.get_or_create(S, Instrument, itype=instrument['itype'])

        # Create Point object
        profile.lat = interpret_coord(profile.lat)
        profile.lon = interpret_coord(profile.lon)
        point = WKTSpatialElement('POINT(%f %f)' % (profile.lon, profile.lat), 4326)
        # print "Creating profile object..."
        # print profile.filename
        # print '-----------------------------------------'

        profile_obj = self.get_or_create(S, Profile,
                              coord=point,
                              date=profile.date,
                              time=profile.time,
                              local_depth=profile.local_depth,
                              instrument=inst_obj.id,
                              cruise=self.cruise_obj.id, # because cruise comes from another function
                              origin_header=str(profile.header),
                              filename=filename)

        date = profile.date.strftime("%d/%m/%Y")
        if not profile_obj.eval_cargo:
            eval_cargo = list("0"*21)
        else:
            eval_cargo = []
            for char in profile_obj.eval_cargo:
                eval_cargo.append(char)

        metadata = [] 
        metalist = [ filename, self.cruise['cruise']['cruise_name'], eval_cargo, 
                     "%0.2f" %(profile.lat), "%0.2f" %(profile.lon),
                     date, self.cruise['cruise']['platform_name'], 
                     instrument['itype'], profile_obj.id ]

        for value in metalist:
            if type(value) == list:
                metadata.extend(value)
            else:
                metadata.append(value)

        self.metadata.append(metadata)

        # ========================================================================================
        # This is a band-aid. We need to figure out how to test it at get_or_create using arrays
        #   We need to try to make a more suitable QUERY that considers arrays comparison
        if not self.data_exists:
            print "NEW %s instance created!" %(ProfileData)
            if instrument['itype'] == 'CTD':
                print " -------------->   Inserting TEMPERATURE data!"
                data_obj = ProfileData(values=profile.temp, 
                                       depths=profile.depth,
                                       status='raw',
                                       variable=temp_obj.id,
                                       profile_id=profile_obj.id)
                S.session.add(data_obj)

                print " -------------->   Inserting SALINITY data!"
                data_obj = ProfileData(values=profile.salt, 
                                       depths=profile.depth,
                                       status='raw',
                                       variable=salt_obj.id,
                                       profile_id=profile_obj.id)
                S.session.add(data_obj)

            elif instrument['itype'] == 'XBT':
                print " -------------->   Inserting TEMPERATURE data!"
                data_obj = ProfileData(values=profile.temp, 
                                       depths=profile.depth,
                                       status='raw',
                                       variable=temp_obj.id,
                                       profile_id=profile_obj.id)
                S.session.add(data_obj)

            elif instrument['itype'] == 'ARGO':
                pass
            else:
                pass
        else:
            print "Instance of %s EXISTS" %(ProfileData)
        # ========================================================================================

        S.session.commit()


    def save_last_loaded(self):
        if "last_cruise.meta" in os.listdir('.'):
            os.remove("last_cruise.meta")
        
        f = open("last_cruise.meta", 'w')
        for line in self.metadata:
            for field in line:
                f.write(str(field) + ";")
            f.write("\n")
        f.close()


class QualifyCruise(object):
    """docstring for Qualify"""
    def __init__(self, cruise_metafile):
        super(QualifyCruise, self).__init__()
        self.cruise = self.load_metafile(cruise_metafile)
        self.instrument = self.cruise[0][-3]
        self.query_profiles()
        
    def load_metafile(self, metafile):
        f = open(metafile)
        cruise = []
        for line in f.readlines():
            cruise.append(line.split(';'))
        return cruise

    def query_profiles(self):
        q = QueryCargoDB()
        self.profiles = q.get_last_cruise(self.cruise)

    def test_single_profile(self, single_profile):
        self.tester = ProfileTests(single_profile, self.instrument, S)
        single_profile[0].profile.eval_cargo = self.tester.eval_cargo

    def test_all_profiles(self):
        report = open('qualify_reports/%s_qualify_report.txt' %(self.cruise[0][1].replace(' ','')), 'w')
        log = open('qualify_reports/%s.log' %(self.cruise[0][1].replace(' ','')), 'w')
        evals_cargo = []

        for p in range(len(self.profiles)):
            report.writelines("\n" + "="*50)
            report.writelines( "\n          TESTING PROFILE %s \n" %self.profiles[p][0].profile.filename )    
            report.writelines("="*50 + "\n")
            tester = self.test_single_profile(self.profiles[p])
            evals_cargo.append(self.tester.eval_cargo) 
            for line in self.tester.output:
                report.writelines(line)
                report.write("\n")
            report.writelines("ERROS: \n")
            for error in self.tester.errors.values():
                report.write(error.encode("utf-8", "replace"))
                report.write("\n")

            report.writelines("\nWARNINGS: \n")
            for warning in self.tester.warnings.values():
                report.write(warning.encode("utf-8", "replace"))
                report.write("\n\n\n")

            report.write("    * --- * --- * --- * --- * --- * --- * --- * --- *    \n")

            for line in self.tester.log:
                log.write(line)
                log.write("\n")

        report.close()
        log.close()
        S.session.commit()
        self.metafile_writer(evals_cargo)
        
    def metafile_writer(self, evals_cargo):

        if "last_cruise.meta" in os.listdir('.'):
            os.remove("last_cruise.meta")

        f = open('last_cruise.meta', 'w')


        first_eval = 2
        last_eval = (first_eval + len(evals_cargo[0])) - 1

        metadata = []
        row = 0

        for station in self.cruise:
            line = []
            col = 0
            for field in station:
                if col >= first_eval and col <= last_eval:
                    line.append(evals_cargo[row][col-first_eval])
                    col += 1
                else:
                    line.append(field)
                    col += 1
                
            metadata.append(line)
            row += 1

        for line in metadata:
            for field in line:
                if field == "\n":
                    pass
                else:
                    f.write(field + ";")
            f.write("\n")


class ExportProfiles(QualifyCruise):
    """docstring for ExportProfiles"""
    def __init__(self, cruise_metafile):
        super(ExportProfiles, self).__init__(cruise_metafile)

    def export_ascii(self, pathname):
        for profile in self.profiles:
            depth = profile[0].depths
            lon = profile[0].profile.coord.coords(S.session)[0]
            lat = profile[0].profile.coord.coords(S.session)[1]
            for profile_data in profile:
                if profile_data.varname.long_name == 'Temperature':
                    temp  = profile_data.values
                elif profile_data.varname.long_name == 'Salinity':
                    salt  = profile_data.values

            with open( "%s/%s.dat" %(pathname, profile[0].profile.filename.split('.')[0]), 'w') as f:
                f.writelines("Coordenadas --> LON: %s ; LAT: %s\n" %(lon, lat))
                f.writelines("Profundidade  Temperatura  Salinidade\n")
                for d, t, s in zip(depth, temp, salt):
                    f.writelines("%0.4f  %0.4f  %0.4f \n" %(d, t, s))

    def export_mat(self, pathname):
        pass

    def export_netcdf(self, pathname):
        pass



class ExportReport(QualifyCruise):
    """docstring for ExportReport"""
    def __init__(self, cruise_metafile):
        super(ExportReport, self).__init__(cruise_metafile)

    def export(self, dirpath, filename):
        origin_dir = "qualify_reports/" 
        report_name = "%s_qualify_report.txt" %self.cruise[0][1].replace(' ','')
        log_name = "%s.log" %self.cruise[0][1].replace(' ','')
        os.system("cp %s%s %s/%s.txt" %(origin_dir, report_name, dirpath, filename) )
        os.system("cp %s%s %s/%s.log" %(origin_dir, log_name, dirpath, filename) )

        

class QueryCargoDB(object):
    def __init__(self):
        pass


    def get_last_cruise(self, metadata):
        # instrument = metadata[-3]
        query = []
        for profile in metadata:
            query.append( S.session.query(ProfileData).filter_by(profile_id=int(profile[-2])).all() )

        return query


    def get_single_profile(self, name):
        q = S.session.query(Profile).filter_by(filename=name).first()
        lon = q.coord.coords(S.session)[0]
        lat = q.coord.coords(S.session)[1]
        print q
        depth = q.data[0].depths
        temp = q.data[0].values
        salt = q.data[1].values

        return np.array(depth), np.array(temp), np.array(salt), lon, lat




        


