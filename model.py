#! -*- coding: utf-8 -*- 
# Modelo PELD
import datetime as dt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, Time, DateTime, ForeignKey, Boolean, Unicode, Sequence, Text, Table
from sqlalchemy import create_engine 
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, backref
from geoalchemy import GeometryColumn, GeometryDDL, Point, Polygon
import platform


if platform.system() == 'Windows':
    engine = create_engine('postgresql://postgres:1234@localhost:5432/peldDB', echo=True)
else:
    engine = create_engine('postgresql://:5432/peldDB', echo=True)

Base = declarative_base()

class SeaPolygon(Base):
    __tablename__ = 'sea'
    """Sea coordinates in the globe"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    poly = GeometryColumn(Polygon(2))

class Meteorologia(Base):
    __tablename__ = 'meteo'
    """Meteorological Parameters"""
    id = Column(Integer, primary_key=True)
    wspd = Column(Float)
    wdir = Column(Float)
    radiation = Column(Float)
    station_id = Column(ForeignKey('station.id'))

class Oceanografia(Base):
    __tablename__ = 'ocean'
    """Oceanographic Parameters"""
    id = Column(Integer, primary_key=True)
    depth = Column(Float)
    temp = Column(Float)
    salt = Column(Float)
    chla = Column(Float)
    feofitina = Column(Float)
    primary_prod = Column(Float)
    bacterian_prod = Column(Float)
    bacterian_biomass = Column(Float)
    org_part_carbon = Column(Float)
    org_diss_carbon = Column(Float)
    station_id = Column(ForeignKey('station.id'))

class Estacao(Base):
    __tablename__ = 'station'
    """Oceanographic Parameters"""
    id = Column(Integer, primary_key=True)
    local_sea = Column(Unicode) # i.e. inner or outer sea
    spot_name = Column(Unicode) # i.e. saco do cardeiro, enseada do forno, etc
    name = Column(Unicode)
    date = Column(Date)
    time = Column(Time)
    local_depth = Column(Float)
    lon = Column(Float)
    lat = Column(Float)
    capture_type = Column(Unicode)
    cruise_id = Column(ForeignKey('cruise.id'))
    meteo = relationship("Meteorologia", uselist=False, backref="station")
    ocean = relationship("Oceanografia", uselist=False, backref="station")
    profile = relationship("Profile", uselist=False, backref="station")
    biometry = relationship("BiometriaIctiofauna", uselist=False, backref="station")

# PRECISO FALAR COM O RICARDO DESSA RELACAO #########################################
class BiometriaIctiofauna(Base):
    __tablename__ = 'biometry'
    """Biometry of Ictiofauna"""
    id = Column(Integer, primary_key=True)
    weight = Column(Float)
    length = Column(Float)
    stomach = relationship("ConteudoEstomacal", uselist=False, backref="biometry")
    station_id = Column(ForeignKey('station.id'))
    organism_id = Column(ForeignKey('organism.id'))

class Organismo(Base):
    __tablename__ = 'organism'
    """Organism Characteristics"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    family = Column(Unicode)
    description = Column(Unicode)
    biometry = relationship("BiometriaIctiofauna", uselist=False, backref="organism")

class ConteudoEstomacal(Base):
    __tablename__ = 'stomach'
    """Stomach contents"""
    id = Column(Integer, primary_key=True)
    contents = Column(Unicode)
    biometry_id = Column(ForeignKey('biometry.id'))
    
#######################################################################################


class Institution(Base):
    __tablename__ = 'institution'
    """Institution responsible for data acquisition"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    cruise = relationship("Cruise", backref="institution")
    project = relationship("Project", backref="institution")

class Project(Base):
    __tablename__ = 'project'
    """Project at which data was acquired"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    institution_id = Column(ForeignKey('institution.id'))
    cruise = relationship("Cruise", backref="project")
    

class Cruise(Base):
    """Each Ship Comission"""
    __tablename__ = 'cruise'
    id = Column(Integer, primary_key=True)
    cruise_name = Column(Unicode) 
    platform_name = Column(Unicode)
    platform_type = Column(Unicode)
    start_date = Column(Date)
    end_date = Column(Date)
    institution_id = Column(ForeignKey('institution.id'))
    project_id = Column(ForeignKey('project.id'))
    station = relationship("Estacao", backref="Station")

class Profile(Base):
    """Profile Table"""
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    time = Column(Time)
    local_depth = Column(Float)
    origin_header = Column(Unicode)
    filename = Column(Unicode)
    created = Column(DateTime, default=dt.datetime.now())
    station_id = Column(ForeignKey('station.id'))
    data = relationship("ProfileData", backref="profile")

class ProfileData(Base):
    """Data Table"""
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    values = Column(postgresql.ARRAY(Float))
    depths = Column(postgresql.ARRAY(Float))
    status = Column(Unicode) # raw, qualified or filtered
    profile_id = Column(ForeignKey('profile.id'))


GeometryDDL(Profile.__table__)
GeometryDDL(ProfileData.__table__)
GeometryDDL(SeaPolygon.__table__)
Base.metadata.create_all(engine)
