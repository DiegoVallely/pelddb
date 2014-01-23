
# Define tables

SeaPolygon = db.define_table("seapolygon",
	Field("name"),
	Field("poly", "geometry()"))

SeaPolygon.insert(poly=geoPolygon((2)))


Station = db.define_table("station",
	Field("local_sea"),
	Field("spot_name"),
	Field("name"),
	Field("date","date"),
	Field("time", "time"),
	Field("local_depth", "double"),
	Field("lon", "double"),
	Field("lat", "double"),
	Field("capture_type"),
	Field("cruise_id", "reference cruise"),
	Field("meteos", "reference meteorology"),
	Field("oceans", "reference oceanography"),
	Field("images", "reference image"),
	Field("profiles", "reference profile"),
	Field("organisms", "reference organisms"),
	Field("biometries", "reference ictiofaunabiometry"))


Meteorology = db.define_table("meteorology",
	Field("wspd", "double"),
	Field("wdir", "double"),
	Field("radiation", "double"),
	Field("station_id", "reference station"))


Oceanography = db.define_table("oceanography",
	Field("depth", "double"),
	Field("temp", "double"),
	Field("salt", "double"),
	Field("chla", "double"),
	Field("feofitina", "double"),
	Field("primary_prod", "double"),
	Field("bacterian_prod", "double"),
	Field("bacterian_biomass", "double"),
	Field("org_part_carbon", "double"),
	Field("org_diss_carbon", "double"),
	Field("station_id", "reference station"))


Image = db.define_table("image",
	Field("pathname"),
	Field("filename"),
	Field("station_id", "reference station"))


Profile = db.define_table("profile",
	Field("time", "time"),
	Field("local_depth", "double"),
	Field("origin_header"),
	Field("filename"),
	Field("created"),
	Field("station_id", "reference station"),
	Field("data", "reference profiledata"))


ProfileData = db.define_table("profiledata",
	Field("values", "list:integer"),
	Field("depths", "list:integer"),
	Field("status"),
	Field("profile_id", "reference profile"))


IctiofaunaBiometry = db.define_table("ictiofaunabiometry",
	Field("weight", "double"),
	Field("lenght", "double"),
	Field("station_id", "reference station"),
	Field("organisms_id", "reference organisms"))


Organisms = db.define_table("organisms",
	Field("name"),
	Field("family"),
	Field("description"),
	Field("station_id", "reference station"),
	Field("biometries", "reference ictiofaunabiometry"),
	Field("stomach", "reference stomachcontents"))


StomachContents = db.define_table("stomachcontents",
	Field("contents"),
	Field("organisms_id", "reference organisms"))


Institution = db.define_table("institution",
	Field("name"),
	Field("cruises", "reference cruise"),
	Field("projects", "reference project"))


Project = db.define_table("project",
	Field("name"),
	Field("institution", "reference institution"),
	Field("cruise", "reference cruise"))


Cruise = db.define_table("cruise",
	Field("name"),
	Field("platform_name"),
	Field("platform_type"),
	Field("start_date", "date"),
	Field("end_date", "date"),
	Field("institution_id", "reference institution"),
	Field("project_id", "reference project"),
	Field("stations", "reference station"))