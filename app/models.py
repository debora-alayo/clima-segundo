from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClimaCiudad(Base):
    __tablename__ = "climaciudad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    temperatura = Column(String)
    precipitacion = Column(String)
    fecha = Column(Date)