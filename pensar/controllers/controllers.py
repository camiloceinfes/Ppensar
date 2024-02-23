from pensar.services.servicePensar import Ppensar
from fastapi import APIRouter, HTTPException, Path
from config.db import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
from typing import Optional
from typing import Union

router_pensar = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class parametros():
#     pass

@router_pensar.get("")
async def tests(code: int, current_year: int, state: str = None,  db: Session = Depends(get_db)):
    test = Ppensar().get_tests(code,current_year,state,db)
    return test

@router_pensar.get("/tasks")
async def test(grado: int, salon: str = None, area: str = None,  db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(grado,salon, area,db)
    return tasks

@router_pensar.get("/results")
async def results(db: Session = Depends(get_db)):
    results = Ppensar().global_results(db)
    return results

@router_pensar.get("/cycle/results")
async def component(db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(db)
    return cycle_results

@router_pensar.get("/components")
async def component(grado: int, salon: str = None, area: str = None, comp: str = None, db: Session = Depends(get_db)):
    pensar = Ppensar().calculate_componentes(grado, salon, area, comp, db)
    return pensar

@router_pensar.get("/competences/{idColegio}")
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


# (idColegio: int, area: Union[str, None] = None, materia: Union[str, None] = None, grado: Union[int, None] = None, db: Session = Depends(get_db)):