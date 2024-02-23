from fastapi import APIRouter, Depends
from config.db import SessionLocal
from pensar.services.servicePensar import Ppensar
from sqlalchemy.orm import Session
from typing import Union
from auth.jwt_bearer import JwtBearer

router_pensar = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# protected_route (authorization header)
@router_pensar.get("/tests", dependencies=[Depends(JwtBearer())] )
async def tests(code: int, current_year: int, state: str = None, db: Session = Depends(get_db)):
    test = Ppensar().get_tests(code, current_year, state, db)
    return test

@router_pensar.get("/tasks", dependencies=[Depends(JwtBearer())])
async def task(grado: int, salon: str = None, area: str = None,  db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(grado, salon, area, db)
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer())])
async def results(db: Session = Depends(get_db)):
    results = Ppensar().global_results(db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer())])
async def component(db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(db)
    return cycle_results

@router_pensar.get("/components", dependencies=[Depends(JwtBearer())])
async def component(grado: int, salon: str = None, area: str = None, comp: str = None, db: Session = Depends(get_db)):
    pensar = Ppensar().calculate_componentes(grado, salon, area, comp, db)
    return pensar

@router_pensar.get("/competences/{idColegio}", dependencies=[Depends(JwtBearer())])
async def competencies(idColegio: int, db: Session = Depends(get_db)):
    _competencias = Ppensar().calculate_competencias(idColegio, db)
    return _competencias

@router_pensar.get("/area", dependencies=[Depends(JwtBearer())])
async def area(idColegio: int, 
               anio: Union[str, None] = None, 
               idPrueba: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _area = Ppensar().calculate_area(idColegio, anio, idPrueba, db)
    return _area
