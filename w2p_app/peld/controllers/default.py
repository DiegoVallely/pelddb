

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
    """Landing Page"""
    return dict()

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
