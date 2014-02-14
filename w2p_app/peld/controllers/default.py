

def custom_button(form):
    # inputname = form.elements(_type="texto")[0]
    # inputname["_required"] = "required"
    # inputname["_style"] = "background:#FA4A81"

    submit_button = form.elements(_type="submit")[0]
    submit_button["_class"] = "btn btn-primary"
    return form

def custom_form(form):
    inputemail = form.elements(_class="string")[0]
    inputemail['_class'] = "form-control"

    inputpasswd = form.elements(_class="password")[0]
    inputpasswd["_class"] = "form-control"

    # labelcheckbox = form.elements(_label="checkbox")
    # labelcheckbox["_class"] = "checkbox"

    return form

def index():
    import datetime as dt
    from read_data.read_data import *
    from dictionaries.dictionaries import spot_dict
    import os

    path = os.path.abspath("applications/peld/data_samples/")


    # EXAMPLE OF TIDBIT DATA INSERTION WORKFLOW
    peld_start_date = dt.date(2013, 10, 1)
    peld_end_date = dt.date(2043, 10, 1)


    tidbit = ReadTidbit(path+"/dados_tidbit_pontadacabeca_nov-09_a_set-11")


    # let's assume that institution, project and cruise were not yet inserted in the database
    # INSERTING INSTITUTION
    ieapm = db.institution.insert(name="IEAPM")
    # INSERTING PROJECT
    peld = db.project.insert(name="PELD", institution_id=ieapm)
    # INSERTING CRUISE
    rede_peld = db.cruise.insert(name="REDE PELD", platform_type="Estação Fixa",
                                platform_name="Tidbit", start_date=peld_start_date,
                                end_date=peld_end_date, institution_id=ieapm,
                                project_id=peld)
    # INSERTING STATION
    ptcabeca = db.station.insert(local_sea=u"Mar de Fora", spot_name="Ponta da Cabeça",
                                start_date=tidbit.dates[0], end_date=peld_end_date,
                                start_time=tidbit.times[0], end_time=None, local_depth=8.,
                                lon=-42.0381, lat=-22.9770, capture_type=u"Senso de Temperatura",
                                cruise_id=rede_peld)
    # INSERTING OCEANOGRAPHIC PARAMETERS
    for sample in range(len(tidbit.temps)):
        s = db.oceanography.insert(dates=tidbit.dates[sample], times=tidbit.times[sample],
                                depths=5., temperature=tidbit.temps[sample], station_id=ptcabeca)    

    # EXAMPLE OF BIOLOGICAL SHEET DATA INSERTION WORKFLOW
    enseada = DataSheet1(path+"/enseada.xls")
    date, spot, station, temp, salt, oxig, fosfate, nitrate, amonium, silicate, chla = enseada.get_data()

    antigos = db.project.insert(name="ANTIGOS", institution_id=ieapm)
    # antigos_cruise = db.cruise.insert(name="ANTIGOS", institution_id=ieapm, project_id=antigos)

    for s in range(len(spot)):
        for key, values in zip(spot_dict.keys(), spot_dict.values()):
            for item in values:
                if item == spot[s]:
                    lon = spot_dict[key][1]
                    lat = spot_dict[key][2]

        st = db.station.insert(local_sea="Mar de Dentro", spot_name=spot[s],
                                name=str(station[s]), lon=lon, lat=lat, capture_type="Biology")

        print st
        d = db.oceanography.insert(dates=date[s], temperature=temp[s], salt=salt[s],
                                    chla=chla[s], oxigen=oxig[s], fosfate=fosfate[s],
                                    nitrate=nitrate[s], amonium=amonium[s], silicate=silicate[s],
                                    station_id=st)
    return locals()


def user():

    forms = auth()
    # inputemail = forms.elements(_class="string")[0]
    # inputemail['_class'] = "form-control"

    # inputpasswd = forms.elements(_class="password")[0]
    # inputpasswd["_class"] = "form-control"

    submit_button = forms.elements(_type="submit")[0]
    submit_button["_class"] = "btn btn-primary btn-block" 

    # email_label = forms.elements("label")[0]
    # email_label["_style"] = "display:none;"

    # email_label2 = forms.elements("label")[1]
    # email_label2["_style"] = "display:none;"

    # email_label3 = forms.elements("label")[2]
    # # email_label3[""] = "Remember Me"
    # email_label3["_class"] = "checkbox"


    # for form_style in forms.elements("form"):
    #     form_style["_class"] = "form-signin"


    # placemail = forms.elements(_type="text")[0]
    # placemail["_placeholder"] = "Email"
    # placepwd = forms.elements(_type="password")[0]
    # placepwd["_placeholder"] = "Password"

    # register_button = forms.add_button(T('Register'), 
    #   URL(args='register', 
    #       vars={'_next': request.vars._next} \
    #       if request.vars._next else None),
    #       _class='btn btn-primary')
    

    return dict(form=forms)


def login():

    form = auth.login()

    return dict(form=form)


def perfil():
    return dict()
