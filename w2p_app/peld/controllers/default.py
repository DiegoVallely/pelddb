
def index():
	form = SQLFORM.grid(SeaPolygon)
	return dict(form=form)

def user():
	return dict(form=auth())