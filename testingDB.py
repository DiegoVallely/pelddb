#! -*- coding: utf-8 -*- 
from model import *
from control import *

class ReadTidbit(object):
    """docstring for ReadTidbit"""
    def __init__(self, filename):
        super(ReadTidbit, self).__init__()
        self.filename = filename
        f = open(filename)
        self.dates, self.times, self.temps = [], [], []
        for line in f.readlines():
            # date
            month = int(line.split("/")[0])
            day   = int(line.split("/")[1])
            year  = int(line.split("/")[2][:4])
            date  = dt.datetime(year, month, day)
            # time
            hour   = int(line.split(" ")[2].split(":")[0])
            minute = int(line.split(" ")[2].split(":")[1])
            time   = dt.time(hour, minute)
            # temperature
            temp = line.split(" ")[-1]
            temp = float(temp.split(",")[0] + "." + temp.split(",")[1][0])

            self.dates.append(date)
            self.times.append(time)
            self.temps.append(temp)


def get_or_create(S, table, **kwargs):
        """ Generic method to get some data from db, if does not exists yet, creates a new record."""
        instance = S.session.query(table).filter_by(**kwargs).first()
        
        if not instance:
            instance = table(**kwargs)
            S.session.add(instance)
            print "NEW %s instance created!" %(table)
            S.session.commit()
        else:
            print "Instance of %s EXISTS" %(table)
        return instance


####################################################################################

# EXAMPLE OF TIDBIT DATA INSERTION WORKFLOW
peld_start_date = dt.date(2013, 10, 1)
peld_end_date = dt.date(2043, 10, 1)

# let's load a sample of tidbit time series, just fresh from the water
tidbit = ReadTidbit("data_samples/dados_tidbit_pontadacabeca_nov-09_a_set-11")

# let's assume that institution, project and cruise were not yet inserted in the database
# INSERTING INSTITUTION
ieapm = get_or_create(S, Institution, name="IEAPM")

    # INSERTING PROJECT
peld = get_or_create(S, Project, name='PELD', institution_id=ieapm.id)

        # INSERTING CRUISE
rede_peld = get_or_create(S, Cruise, name=u'REDE PELD', platform_type=u'Estação Fixa', 
                   platform_name=u'Tidbit', start_date=peld_start_date, 
                   end_date=peld_end_date, institution_id=ieapm.id, project_id=peld.id)

            # INSERTING STATION
ptcabeca = get_or_create(S, Station, local_sea="Mar de Fora", spot_name=u"Ponta da Cabeça", 
                   start_date=tidbit.dates[0], start_time=tidbit.times[0],
                   end_date=tidbit.dates[-1], end_time=tidbit.times[-1], local_depth=8., 
                   lon=-42.0, lat=-23.1, capture_type='Sensor de Temperatura', 
                   cruise_id=rede_peld.id)
                
                # INSERTING OCEANOGRAPHIC PARAMETERS
# and now we insert the entire time series sample by sample
print "\n\n Inserting tidbit data sample ....."
for sample in range(len(tidbit.temps)):
    s = get_or_create(S, Oceanography, date=tidbit.dates[sample], time=tidbit.times[sample], 
                     depth=5., temp=tidbit.temps[sample], station_id=ptcabeca.id)

S.session.commit()
