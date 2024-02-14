from sqlalchemy import  Column, Integer, String #, ForeignKey, Float
from app.config.db import Base

class pensar(Base):
    __tablename__ ="pensar"

    ID             = Column(Integer, primary_key=True)
    IDplantel      = Column(Integer)
    nombre_plantel = Column(String(255))
    año_ciclo      = Column(Integer)
    componente     = Column(String(255))
    grado          = Column(Integer)
    salon          = Column(String(255))
    area           = Column(String(255))
    tipo_rejilla   = Column(String(255))
    ciclo_actual_plantel    = Column(Integer)
    ciclo_anterior_plantel  = Column(Integer)
    ciclo_actual_nacional   = Column(Integer)
    ciclo_anterior_nacional = Column(Integer)