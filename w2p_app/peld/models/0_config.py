# -*- coding:utf-8 -*-
from gluon.storage import Storage
from gluon.dal import DAL, Field, geoPoint, geoLine, geoPolygon

config = Storage(db=Storage(),
	auth=Storage(settings=Storage(extra_fields=Storage()),
		message=Storage()),
	mail=Storage())


# - VERY IMPORTANT:
# for there no conflicts between angular.js and web2py, is necessary modified
# the delimiters of the web2py because Angular.js use {{}} too
# response.delimiters = ('{%','%}')


# The database connection
# The string connection id needed change when site be deployed
# need create postgres db without user and password for now
config.db.uri = "postgres://peld:h4ck3r@localhost:5432/pelddb"
# config.db.uri = "sqlite://pelddb.sqlite" 
# Check reserved
config.db.check_reserved = ['all']


# config.auth
config.auth.settings.formstyle = "divs"
config.auth.settings.registration_requires_verification = False
config.auth.settings.registration_requires_approval = False
config.auth.settings.login_after_registration = False
config.auth.settings.login_next = URL('perfil')


config.auth.settings.extra_fields.auth_user = [
	Field("thumbnail", "upload")]


# mail
# config.mail.server = ""
# config.mail.sender = ""
# config.mail.login = ""



# initialize current
from gluon import current
current.config = config

