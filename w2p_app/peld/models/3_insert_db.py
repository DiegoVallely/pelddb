# from model import *
# from control import *
# import datetime as dt
# from read_data.read_data import *
# from dictionaries.dictionaries import spot_dict
# import os

# path = os.path.abspath("applications/peld/data_samples")


# # EXAMPLE OF TIDBIT DATA INSERTION WORKFLOW
# peld_start_date = dt.date(2013, 10, 1)
# peld_end_date = dt.date(2043, 10, 1)


# tidbit = ReadTidbit(path+"/dados_tidbit_pontadacabeca_nov-09_a_set-11")


# # let's assume that institution, project and cruise were not yet inserted in the database
# # INSERTING INSTITUTION

# ieapm = db.institution.insert(name="IEAPM")
# print ieapm
# # peld = db.project.insert(name="PELD", institution_id=ieapm)