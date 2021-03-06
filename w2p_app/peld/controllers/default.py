 # -*- coding: utf-8 -*-
from plugin_paginator import Paginator, PaginateSelector, PaginateInfo
from gluon.contrib.populate import populate

def call():
    session.forget()
    return service()

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
    from insert_db.insert_db import InsertDB

    DB = InsertDB(db)
    # DB.set_data()

    return locals()


def user():

    forms = auth()
    # inputemail = forms.elements(_class="string")[0]
    # inputemail['_class'] = "form-control"

    # inputpasswd = forms.elements(_class="password")[0]
    # inputpasswd["_class"] = "form-control"

    submit_button = forms.elements(_type="submit")[0]
    submit_button["_class"] = "btn btn-primary btn-block" 

    email_label = forms.elements("label")[0]
    email_label["_style"] = "display:none;"

    email_label2 = forms.elements("label")[1]
    email_label2["_style"] = "display:none;"

    # email_label3 = forms.elements("label")[2]
    # # email_label3[""] = "Remember Me"
    # email_label3["_class"] = "checkbox"


    # for form_style in forms.elements("form"):
    #     form_style["_class"] = "form-signin"


    placemail = forms.elements(_type="text")[0]
    placemail["_placeholder"] = "Email"
    placepwd = forms.elements(_type="password")[0]
    placepwd["_placeholder"] = "Password"

    # register_button = forms.add_button(T('Register'), 
    #   URL(args='register', 
    #       vars={'_next': request.vars._next} \
    #       if request.vars._next else None),
    #       _class='btn btn-primary')
    

    return dict(form=forms)


def login():

    form = auth.login()

    return dict(form=form)


@auth.requires_login()
def perfil():

    result = None

    # form = SQLFORM.factory(Field('name', requires=IS_NOT_EMPTY()))
    form = FORM('Pesquisa:',
                INPUT(_type="text", _name="result", requires=IS_NOT_EMPTY(),
                    _id="result", _autocomplete="off", 
                    _onkeyup="getData(this.value);"),
                INPUT(_type="submit"))
    if form.accepts(request):
        tokens = form.vars.result.split()
        query = reduce(lambda a,b:a&b,
            [Institution.name.contains(k) | Project.name.contains(k) \
             for k in tokens])
        result = db(query).select(orderby=db.institution.name)
    # else:
    #     result = DIV(T("Pesquise uma Instituição"),
    #                 _class="alert alert-info")

    submit_button = form.elements(_type="submit")[0]
    submit_button["_class"] = "btn btn-primary"

    inputext = form.elements(_type="text")[0]
    inputext['_class'] = "form-control"

    return dict(form=form, result=result)

@auth.requires_login()
def ajaxlivesearch():
    tokens = request.vars.tokens if request.vars else None
    query = Institution.name.like('%'+tokens+'%')
    # query = reduce(lambda a,b:a&b,
    #         [Institution.name.contains(k) | Project.name.contains(k) \
    #          for k in tokens])
    results = db(query).select(orderby=Institution.name)
    items = []
    for (i,found) in enumerate(results):
        items.append(DIV(A(found.name, _id="res%s"%i, _href="#", 
                    _onclick="copyToBox($('#res%s').html())"%i), 
                    _id="resultLiveSearch"))

    return TAG[''](*items)


@auth.requires_login()
def ocean():
    headers={'oceanography.id':'#','oceanography.dates':'Data', 
            'oceanography.times':'Hora','oceanography.depths':'Profundidade', 
            'oceanography.temperature':'Temperatura','oceanography.salt':'Salinidade',
            'oceanography.chla':'CHLA','oceanography.feofitina':'Feofitina',
            'oceanography.primary_prod':'Produção Primária',
            'oceanography.bacterian_prod':'Produção Bacteriana',
            'oceanography.bacterian_biomass':'Biomassa Bacteriana',
            'oceanography.org_part_carbon':'Carbono Orgânico Particulado',
            'oceanography.org_diss_carbon':'Carbono Orgânico Dissolvido',
            'oceanography.oxigen':'Oxigênio','oceanography.fosfate':'Fosfato',
            'oceanography.nitrate':'Nitrato','oceanography.amonium':'Amônia',
            'oceanography.silicate':'Silicato'}
    
    args = request.args(0)
    query = Oceanography
    qry = db(query).select()

    datas = SQLFORM.grid(query=query, user_signature=True,
            headers=headers, formstyle='divs', create=False, deletable=False,
            editable=False)
    
    paginate_selector = PaginateSelector(anchor='main')
    paginator = Paginator(paginate=paginate_selector.paginate, 
                          extra_vars={'v':1}, anchor='main',
                          renderstyle=True) 
    paginator.records = db(query).count()
    paginate_info = PaginateInfo(paginator.page, paginator.paginate, paginator.records)
    
    rows = db(query).select(limitby=paginator.limitby()) 


    return locals()

def projects():
    args = request.args(0)
    # query = db(Oceanography).select()
    # datas = SQLFORM.grid(query=query, user_signature=True,
    #         headers=headers, formstyle='divs', create=False, deletable=False,
    #         editable=False)

    # if request.args(0) == ''
    query = Oceanography.station_id
    
    paginate_selector = PaginateSelector(anchor='main')
    paginator = Paginator(paginate=paginate_selector.paginate, 
                          extra_vars={'v':1}, anchor='main',
                          renderstyle=True) 
    paginator.records = db(query).count()
    paginate_info = PaginateInfo(paginator.page, paginator.paginate, paginator.records)
    
    rows = db(query).select(limitby=paginator.limitby())

    return locals()

def advancedsearch():
    return locals()


def datainfo():
    inf = request.args(0) or redirect(URL('datas'))
    rows = Oceanography(Oceanography.id == inf)


    return locals()