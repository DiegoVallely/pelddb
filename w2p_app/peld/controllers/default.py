
def index():
	form = SQLFORM.smartgrid(Station)
	return dict(form=form)

def user():
	return dict(form=auth())