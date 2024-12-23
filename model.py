##########
# MODELS #
##########

from sqlalchemy import (
    DateTime,
    Text,
    create_engine,
    select,
    Integer,
    Column,
    String,
    VARCHAR,
    ForeignKey,
    Float,
    Boolean,
)
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from geoalchemy2 import Geometry
from sqlalchemy.sql import func

db_connection = "postgresql://postgres:root@localhost:5432/postgres"
engine = create_engine(db_connection, echo=False)

Session = sessionmaker(engine)
session = Session()

base = declarative_base()


# class NotamEntry(base):
#     __tablename__ = "notam_entry"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     series = Column(String(50), nullable=False)
#     number = Column(String(50), nullable=False) 
#     type = Column(String(50), nullable=False)
#     additional_info = Column(String(50), nullable=True)
#     fir = Column(String(255), nullable=False) 
#     # fir2 = Column(String(50), nullable=True) 
#     # fir3 = Column(String(50), nullable=True)
#     qualifier = Column(String(50), nullable=True) 
#     qualifier1 = Column(String(50), nullable=True) 
#     qualifier2 = Column(String(50), nullable=True)
#     traffic = Column(String(500), nullable=True) 
#     # traffic2 = Column(String(50), nullable=True)
#     purpose = Column(String(500), nullable=True)
#     # purpose2 = Column(String(50), nullable=True)
#     # purpose3 = Column(String(50), nullable=True)
#     scope = Column(String(500), nullable=True)
#     # scope2 = Column(String(50), nullable=True)
#     from_fl = Column(String(500), nullable=True)
#     upto_fl = Column(String(500), nullable=True)
#     center_lat = Column(String(500), nullable=True)
#     center_lon = Column(String(500), nullable=True)
#     radius_of_area_affected = Column(String(255), nullable=True)
#     airport_fir = Column(String(255), nullable=True)
#     # airport_fir2 = Column(String(50), nullable=True)
#     # airport_fir3 = Column(String(50), nullable=True)
#     # airport_fir4 = Column(String(50), nullable=False)
#     start_date = Column(String(500), nullable=False)
#     end_date = Column(String(500), nullable=False) 
#     day_time = Column(String(500), nullable=True)
#     text_description = Column(Text, nullable=True)
#     upper_limit = Column(String(500), nullable=True)
#     lower_limit = Column(String(500), nullable=True)
#     created_on = Column(String(500), nullable=False)
#     source = Column(String(1000), nullable=True)
#     notam = Column(String(3000), nullable=True)
   
    
class NotamEntry(base):
    __tablename__ = "notam_entry"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series = Column(String(50), nullable=True)
    number = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    additional_info = Column(String(500), nullable=True)
    fir = Column(String(500), nullable=False)
    qualifier = Column(String(500), nullable=True)
    qualifier1 = Column(String(500), nullable=True)
    qualifier2 = Column(String(500), nullable=True)
    traffic = Column(String(500), nullable=True)
    purpose = Column(String(500), nullable=True)
    scope = Column(String(500), nullable=True)
    from_fl = Column(String(500), nullable=True)
    upto_fl = Column(String(500), nullable=True)
    center_lat = Column(String(500), nullable=True)
    center_lon = Column(String(500), nullable=True)
    radius_of_area_affected = Column(String(500), nullable=True)
    airport_fir = Column(String(500), nullable=True)
    start_date = Column(String(500), nullable=False)
    end_date = Column(String(500), nullable=False)
    day_time = Column(Text, nullable=True)  # Use Text for longer time strings
    text_description = Column(Text, nullable=True)  # Unlimited length
    upper_limit = Column(String(500), nullable=True)
    lower_limit = Column(String(500), nullable=True)
    created_on = Column(String(500), nullable=False)
    source = Column(Text, nullable=True)  # Unlimited length
    notam = Column(Text, nullable=True)  # Unlimited length

# Series Table
class Series(base):
    __tablename__ = 'series'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer,primary_key=False)  
    series = Column(String(50), nullable=False)  
    name = Column(String(1000), nullable=False)  
    subject = Column(String(1000), nullable=True)

# Type Table
class Type(base):
    __tablename__ = 'type'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer,primary_key=False)   
    type = Column(String(50), nullable=False)  
    name = Column(String(1000), nullable=False)  
    subject = Column(String(2550), nullable=True)  

# Traffic Table
class Traffic(base):
    __tablename__ = 'traffic'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer,primary_key=False)    
    traffic = Column(String(50), nullable=False)  
    name = Column(String(1000), nullable=False)  

# Purpose Table
class Purpose(base):
    __tablename__ = 'purpose'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer,primary_key=False)   
    purpose = Column(String(50), nullable=False)  
    name = Column(String(1000), nullable=False)  

# Scope Table
class Scope(base):
    __tablename__ = 'scope'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer,primary_key=False)   
    scope = Column(String(50), nullable=False)  
    name = Column(String(1000), nullable=False)  
    

# GeneralInstruction table
class GeneralInstruction(base):
    __tablename__ = 'generalinstruction'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)
    significance = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=func.now())  
    
# SecondAndThirdLetterDecode table
class SecondAndThirdLetterDecode(base):
    __tablename__ = 'secondandthirdletterdecode'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    code = Column(String(50), nullable=False)
    significance = Column(String(255), nullable=False)   
    uniform_abbreviated_phraseology = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    

# FourthAndFifthLetterDecode table
class FourthAndFifthLetterDecode(base):
    __tablename__ = 'fourthandfifthletterdecode'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)
    significance = Column(String(1000), nullable=False)   
    uniform_abbreviated_phraseology = Column(String(1000), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=func.now()) 
    
    
# Minima data

# Dest Enr Minima
class DestEnrMinima(base):
    __tablename__ = 'dest_enr_minima'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer, nullable=False)
    icao_code = Column(String(10), nullable=True)
    rwy = Column(String(20), nullable=True)
    procedure_type = Column(String(50), nullable=True)
    procedure = Column(String(100), nullable=True)
    procedure_condition = Column(String(100), nullable=True)
    acft_cat = Column(String(10), nullable=True)
    acft_type = Column(String(255), nullable=True)
    als_type =Column(String(255), nullable=True)
    ra = Column(String(255), nullable=True)
    mda = Column(String(255), nullable=True)
    mdh = Column(String(255), nullable=True)
    da = Column(String(255), nullable=True)
    dh = Column(String(255), nullable=True)
    rvr_als = Column(String(255), nullable=True)
    vis_als = Column(String(255), nullable=True)
    rvr_without_als = Column(String(255), nullable=True)
    vis_without_als = Column(String(255), nullable=True)
    remarks = Column(String(255), nullable=True)
    airline = Column(String(255), nullable=True)
    cmv_day = Column(String(255), nullable=True)
    cmv_night = Column(String(255), nullable=True)
    

#take off 
class TakeOffMinima(base):
    __tablename__ = 'take_off_minima'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer, nullable=False)
    icao_code = Column(String(10), nullable=True)
    runway = Column(String(20), nullable=True)
    lvto_rvr_vis = Column(String(255), nullable=True)
    non_lvto_rvr_vis = Column(String(255), nullable=True)
    
# take off alt minima
class TakeOffAltMinima(base):
    __tablename__ = 'take_off_alt_minima'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer, nullable=False)
    icao_code = Column(String(10), nullable=True)
    icao_altn = Column(String(10), nullable=True)
    rvr_vis = Column(String(255), nullable=True)
    
#dest alt minima
class DestAltMinima(base):
    __tablename__ = 'dest_alt_minima'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial_number = Column(Integer, nullable=False)
    icao_code = Column(String(10), nullable=True)
    dh = Column(String(255), nullable=True)
    mdh = Column(String(255), nullable=True)

   
    