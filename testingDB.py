from control import *



# INSERTING INSTITUTIONS
ieapm = Institution(name='IEAPM')
S.session.add(ieapm)
S.session.commit()



	# INSERTING PROJECT
peld = Project(name='PELD', institution_id=ieapm.id)
S.session.add(peld)
S.session.commit()

		# INSERTING CRUISES
pilot = Cruise(cruise_name='PILOT', platform_type='Boat', platform_name='Leg',
	           start_date=dt.date(2014, 01, 01), end_date=dt.date(2014, 01, 10), 
	           institution_id=ieapm.id, project_id=peld.id)
S.session.add(pilot)
S.session.commit()


			# INSERTING STATIONS
s1 = Estacao(date=dt.date(2014, 01, 01), time=dt.time(10, 30, 0), local_depth=100., 
	               lon=-42.0, lat=-23.1, capture_type='Arrasto', cruise_id=pilot.id)
S.session.add(s1)
S.session.commit()
				
				# INSERTING OCEANOGRAPHIC PARAMETERS
o1 = Oceanografia(depth=10., temp=23.4, salt=36.78, chla=0.5564, feofitina=6.7, 
	              primary_prod=30.9, bacterian_prod=0.88, bacterian_biomass=None, 
	              org_part_carbon=None, org_diss_carbon=0.000342, station_id=s1.id)
S.session.add(o1)
S.session.commit()

				# INSERTING METEOROLOGICAL PARAMETERS
m1 = Meteorologia(wspd=8.5, wdir=82., radiation=None, station_id=s1.id)
S.session.add(m1)
S.session.commit()

s2 = Estacao(date=dt.date(2014, 01, 01), time=dt.time(11, 30, 0), local_depth=120., 
	               lon=-42.0, lat=-23.1, capture_type='Arrasto', cruise_id=pilot.id)
S.session.add(s2)
S.session.commit()


peld1 = Cruise(cruise_name='PELD1', platform_type='Boat', platform_name='Leg',
	           start_date=dt.date(2014, 02, 01), end_date=dt.date(2014, 02, 10), 
	           institution_id=ieapm.id, project_id=peld.id)
S.session.add(peld1)
S.session.commit()


	# INSERTING PROJECT
inct = Project(name='INCT', institution_id=ieapm.id)
S.session.add(inct)
S.session.commit()

		# INSERTING CRUISES
inct1 = Cruise(cruise_name='INCT1', platform_type='Ship', platform_name='Diadorim',
	           start_date=dt.date(2013, 01, 01), end_date=dt.date(2013, 01, 10), 
	           institution_id=ieapm.id, project_id=inct.id)
S.session.add(inct1)
S.session.commit()

inct2 = Cruise(cruise_name='INCT2', platform_type='Ship', platform_name='Diadorim',
	           start_date=dt.date(2013, 02, 01), end_date=dt.date(2013, 02, 10), 
	           institution_id=ieapm.id, project_id=inct.id)
S.session.add(inct2)
S.session.commit()






S.session.commit()
