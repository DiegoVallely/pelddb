

# BioFile = db.define_table("biofile",
#   Field("name", requires=IS_NOT_EMPTY(error_message="Nome!")),
#   Field("filename", "upload"))


SeaPolygon = db.define_table("seapolygon",
    Field("name"),
    Field("poly", "geometry()"),
    format="%(name)s")


Institution = db.define_table("institution",
    Field("name"),
    # Field("biofile_id", "reference biofile"),
    format="%(name)s")

Project = db.define_table("project",
    Field("name"),
    Field("institution_id", "reference institution"),
    format="%(name)s")

Cruise = db.define_table("cruise",
    Field("name"),
    Field("platform_type"),
    Field("start_date", "date"),
    Field("end_date", "date"),
    Field("institution_id", "reference institution"),
    format="%(name)s")

Station = db.define_table("station",
    Field("local_sea", "string"),
    Field("spot_name", "string"),
    Field("date_", "date"),
    Field("time_", "time"),
    Field("lon", "double"),
    Field("lat", "double"),
    Field("capture_type", "string"),
    Field("cruise_id", "reference cruise"))

Meteorology = db.define_table("meteorology",
    Field("wspd", "double"),
    Field("wdir", "double"),
    Field("radiation", "double"),
    Field("station_id", "reference station"))

Image = db.define_table("image",
    Field("filename", "upload"))

Oceanography = db.define_table("oceanography",
    Field("dates", "date"),
    Field("times", "time"),
    Field("depths", "double"),
    Field("temperature", "double"),
    Field("salt", "double"),
    Field("chla", "double"),
    Field("feofitina", "double"),
    Field("primary_prod", "double"),
    Field("bacterian_prod", "double"),
    Field("bacterian_biomass", "double"),
    Field("org_part_carbon", "double"),
    Field("org_diss_carbon", "double"),
    Field("oxigen", "double"),
    Field("fosfate", "double"),
    Field("nitrate", "double"),
    Field("amonium", "double"),
    Field("silicate", "double"),
    Field("station_id", "reference station"))

Profile = db.define_table("profile",
    Field("coord", "double"),
    Field("times", "time"),
    Field("local_depth", "double"),
    Field("origin_header", "string"),
    Field("filename", "string"),
    Field("created", "date"),
    Field("station_id", "reference station"))

ProfileData = db.define_table("profiledata",
    Field("values_", "list:string"),
    Field("depths", "list:string"),
    Field("status", "string"),
    Field("variable_name"),
    Field("profile_id", "reference profile"))

Organisms = db.define_table("organisms",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("familys", "string"),
    Field("description", "string"),
    Field("station_id", "reference station"),
    format="%(name)s")

StomachContents = db.define_table("stomachcontents",
    Field("contents"),
    Field("organisms_id", "reference organisms"),
    format="%(contents)s")

IctiofaunaBiometry = db.define_table("ictiofaunabiometry",
    Field("weight", "double"),
    Field("lenght", "double"),
    Field("organisms_id", "reference organisms"))