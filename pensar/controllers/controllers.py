from fastapi import APIRouter, Depends, HTTPException, status
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
@router_pensar.get("/global-params", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Resource not found"},
    500: {"description": "Internal Server Error"}
})
async def global_params(code: int, year: int, db: Session = Depends(get_db)):
    global_params = Ppensar().get_global_params(code, year, db)
    
    if not global_params:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return global_params

@router_pensar.get("/tests", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK )
async def tests(code: int, year: int, db: Session = Depends(get_db)):
    test = Ppensar().get_tests(code, year, db)
    return test

@router_pensar.get("/tasks", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Tasks not found"},
    500: {"description": "Internal Server Error"}
})
async def task(code: int, year: int,  idGrade: int, idClassroom: int = None, idPrueba: int = None, idArea: int = None, db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(code, year, idGrade, idClassroom, idPrueba, idArea, db)
    
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer())])
async def results(db: Session = Depends(get_db)):
    results = Ppensar().global_results(db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer())])
async def component(db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(db)
    return cycle_results

@router_pensar.get("/componente", dependencies=[Depends(JwtBearer())])
async def component(idColegio: int = None,
                    grado: int = None, salon: str = None, 
                    area: str = None, comp: str = None, 
                    db: Session = Depends(get_db)):
    pensar = Ppensar().calculate_componentes(idColegio, grado, salon, area, comp, db)
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

@router_pensar.get("/grado", dependencies=[Depends(JwtBearer())])
async def grado(idColegio: int, 
               anio: Union[str, None] = None, 
               idArea: Union[int, None] = None, 
               idPrueba: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _grado = Ppensar().calculate_grado(idColegio, anio, idPrueba, idArea, db) #= pns().competencias(idColegio, db) código de colegio, año actual, id_area, id_prueba
    return _grado

# (idColegio: int, area: Union[str, None] = None, materia: Union[str, None] = None, grado: Union[int, None] = None, db: Session = Depends(get_db)):
