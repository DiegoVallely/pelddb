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



# EXAMPLE OF TIDBIT DATA INSERTION WORKFLOW
peld_start_date = dt.date(2013, 10, 1)
peld_end_date = dt.date(2043, 10, 1)

# let's load a sample of tidbit time series, just fresh from the water
tidbit = ReadTidbit("data_samples/dados_tidbit_pontadacabeca_nov-09_a_set-11")

# let's assume that institution, project and cruise were not yet inserted in the database
# INSERTING INSTITUTION
ieapm = Institution(name='IEAPM')
S.session.add(ieapm)
S.session.commit()

    # INSERTING PROJECT
peld = Project(name='PELD', institution_id=ieapm.id)
S.session.add(peld)
S.session.commit()

        # INSERTING CRUISE
rede_peld = Cruise(name=u'REDE PELD', platform_type=u'Estação Fixa', platform_name=u'Tidbit',
                   start_date=peld_start_date, end_date=peld_end_date, 
                   institution_id=ieapm.id, project_id=peld.id)
S.session.add(rede_peld)
S.session.commit()

            # INSERTING STATION
ptcabeca = Station(local_sea="Mar de Fora", spot_name=u"Ponta da Cabeça", 
                   start_date=tidbit.dates[0], start_time=tidbit.times[0],
                   end_date=tidbit.dates[-1], end_time=tidbit.times[-1], local_depth=8., 
                   lon=-42.0, lat=-23.1, capture_type='Sensor de Temperatura', 
                   cruise_id=rede_peld.id)
S.session.add(ptcabeca)
S.session.commit()
                
                # INSERTING OCEANOGRAPHIC PARAMETERS

# and now we insert the entire time series sample by sample
for sample in range(len(tidbit.temps)):
    s = Oceanography(date=tidbit.dates[sample], time=tidbit.times[sample], 
                     depth=5., temp=tidbit.temps[sample], station_id=ptcabeca.id)
    S.session.add(s)
    S.session.commit()


S.session.commit()
