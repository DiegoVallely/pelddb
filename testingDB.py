#! -*- coding: utf-8 -*- 
from model import *
from control import *
from read_data import *
from dictionaries import spot_dict

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

# bbox for peld area
# m1 = Basemap(projection='cyl', llcrnrlon=-42.2, urcrnrlon=-41.7,
                    # llcrnrlat=-23.144, urcrnrlat=-22.5, lat_ts=0, resolution='f')

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
                   end_date=peld_end_date, end_time=None, local_depth=8., 
                   lon=-42.0381, lat=-22.9770, capture_type='Sensor de Temperatura', 
                   cruise_id=rede_peld.id)
                
                # INSERTING OCEANOGRAPHIC PARAMETERS
# and now we insert the entire time series sample by sample
print "\n\n Inserting tidbit data sample ....."
for sample in range(len(tidbit.temps)):
    s = get_or_create(S, Oceanography, date=tidbit.dates[sample], time=tidbit.times[sample], 
                     depth=5., temp=tidbit.temps[sample], station_id=ptcabeca.id)





# EXAMPLE OF BIOLOGICAL SHEET DATA INSERTION WORKFLOW
enseada = DataSheet1('data_samples/enseada.xls')
date, spot, station, temp, salt, oxig, fosfate, nitrate, amonium, silicate, chla = enseada.get_data()

    # INSERTING PROJECT: for old data that has unknown info
antigos = get_or_create(S, Project, name='ANTIGOS', institution_id=ieapm.id)

for s in range(len(spot)):
    for key, values in zip(spot_dict.keys(), spot_dict.values()):
        for item in values:
            if item == spot[s]:
                lon = spot_dict[key][1]
                lat = spot_dict[key][2]

    st = get_or_create(S, Station, local_sea="Mar de Dentro", spot_name=spot[s], 
                       name=str(station[s]), lon=lon, lat=lat, capture_type="Biology")

    d = get_or_create(S, Oceanography, date=date[s], temp=temp[s], salt=salt[s], 
                      chla=chla[s], oxigen=oxig[s], fosfate=fosfate[s], nitrate=nitrate[s], 
                      amonium=amonium[s], silicate=silicate[s], station_id=st.id)



S.session.commit()