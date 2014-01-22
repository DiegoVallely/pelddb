# -*- coding: utf-8 -*-
from gluon.custom_import import track_changes
track_changes(True)

from gluon.contrib.markdown.markdown2 import markdown
from gluon.tools import Auth, Service, Crud

from gluon.dal import DAL, Field, geoPoint, geoLine, geoPolygon


service = Service()
private_service = Service()

# generator for database connection
db = DAL(**config.db)
crud = Crud(db)


# the settings for model and auth
auth = Auth(db, hmac_key=Auth.get_or_create_key())
auth.settings.formstyle = config.auth.settings.formstyle
auth.settings.extra_fields['auth_user'] = \
	config.auth.settings.extra_fields.auth_user
# auth.settings.mailer = mail
auth.settings.registration_requires_verification = \
	config.auth.settings.registration_requires_verification
auth.settings.registration_requires_approval = \
	config.auth.settings.registration_requires_approval
auth.settings.login_after_registration = \
	config.auth.settings.login_after_registration

# auth.messages.registration_successful = \
	# config.auth.messages.registration_successful


auth.define_tables()
