from pensar.services.servicePensar import Ppensar
from fastapi import APIRouter, HTTPException, Path
from config.db import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
from typing import Union

router_pensar = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_pensar.get("/componente")
async def component(idColegio: int = None,
                    grado: int = None, salon: str = None, 
                    area: str = None, comp: str = None, 
                    db: Session = Depends(get_db)):
    pensar = Ppensar().calculate_componentes(idColegio, grado, salon, area, comp, db)
    return pensar

@router_pensar.get("/competencias/{idColegio}")
async def competencies(idColegio: int, db: Session = Depends(get_db)):
    _competencias = Ppensar().calculate_competencias(idColegio, db)
    return _competencias

@router_pensar.get("/area")
async def area(idColegio: int, 
               anio: Union[str, None] = None, 
               idPrueba: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _area = Ppensar().calculate_area(idColegio, anio, idPrueba, db) #= pns().competencias(idColegio, db) código de colegio, año actual, id_area, id_prueba
    return _area

@router_pensar.get("/grado")
async def grado(idColegio: int, 
               anio: Union[str, None] = None, 
               idArea: Union[int, None] = None, 
               idPrueba: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _grado = Ppensar().calculate_grado(idColegio, anio, idPrueba, idArea, db) #= pns().competencias(idColegio, db) código de colegio, año actual, id_area, id_prueba
    return _grado

# (idColegio: int, area: Union[str, None] = None, materia: Union[str, None] = None, grado: Union[int, None] = None, db: Session = Depends(get_db)):