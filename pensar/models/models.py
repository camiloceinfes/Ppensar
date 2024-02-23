from sqlalchemy import  Column, Integer, String, Float
from config.db import Base

class componentes_model(Base):
    __tablename__ ="componentes"

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

class competencias_model(Base):
    __tablename__ ="competencias"
    #_table_args__ ={'schema': 'BD_MARTESDEPRUEBA.dbo'}

    ID           = Column(Integer, primary_key= True)
    IDplantel    = Column(Integer)
    año          = Column(Integer)
    departamento = Column(String(255))
    ciudad       = Column(String(255))
    competencia  = Column(String(255))
    componente   = Column(String(255))
    area                  = Column(String(255))
    materia               = Column(String(255))
    nombrePrueba          = Column(String(255))
    grado                 = Column(Integer)
    pregunta_Estado       = Column(String(255))
    porcentaje_de_acierto = Column(Float)
    
class Pensar(Base):
    __tablename__ ="pensar"
    #_table_args__ ={'schema': 'BD_MARTESDEPRUEBA.dbo'}

    ID           = Column(Integer, primary_key= True)
    IDplantel    = Column(Integer)
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
