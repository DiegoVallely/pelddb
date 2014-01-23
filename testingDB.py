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
peld = Cruise(name='PELD', platform_type='Estação Fixa', platform_name='Tidbit',
	           start_date=dt.date(2014, 01, 01), end_date=dt.date(2014, 01, 10), 
	           institution_id=ieapm.id, project_id=peld.id)
S.session.add(pilot)
S.session.commit()


			# INSERTING STATIONS
ptcab = Station(local_sea="Mar de Fora", spot_name="Ponta da Cabeça", date=dt.date(2014, 01, 01), time=dt.time(10, 30, 0), local_depth=100., 
	               lon=-42.0, lat=-23.1, capture_type='Arrasto', cruise_id=peld.id)
S.session.add(s1)
S.session.commit()
				
				# INSERTING OCEANOGRAPHIC PARAMETERS
o1 = Oceanography(depth=10., temp=23.4, salt=36.78, chla=0.5564, feofitina=6.7, 
	              primary_prod=30.9, bacterian_prod=0.88, bacterian_biomass=None, 
	              org_part_carbon=None, org_diss_carbon=0.000342, station_id=s1.id)
S.session.add(o1)
S.session.commit()


S.session.commit()
