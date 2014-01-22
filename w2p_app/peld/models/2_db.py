
# Define tables

SeaPolygon = db.define_table("seapolygon",
	Field("name"),
	Field("poly", "geometry()"))

SeaPolygon.insert(poly=geoPolygon((2)))