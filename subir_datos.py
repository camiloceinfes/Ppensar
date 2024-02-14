import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la base para las clases de mapeo
Base = declarative_base()

# Definir la clase que mapea a la tabla pensar
class Pensar(Base):
    __tablename__ = 'pensar'
    ID = Column(Integer, primary_key=True)
    IDplantel = Column(Integer)
    nombre_plantel = Column(String)
    año_ciclo = Column(Integer)
    componente = Column(String)
    grado = Column(String)
    salon = Column(String)
    area = Column(String)
    tipo_rejilla = Column(String)
    ciclo_actual_plantel = Column(String)
    ciclo_anterior_plantel = Column(String)
    ciclo_actual_nacional = Column(String)
    ciclo_anterior_nacional = Column(String)


DATABASE_URL = "postgresql://postgres:950221@127.0.0.1/Ppensar"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

datos_excel = pd.read_excel(r"C:\Users\Camilo\Desktop\base de datos.xlsx")

session = SessionLocal()
for indice, fila in datos_excel.iterrows():
    registro = Pensar(**fila.to_dict())
    session.add(registro)
session.commit()
session.close()
