from fastapi import APIRouter, Depends, HTTPException, status
from config.db import SessionLocal
from pensar.services.servicePensar import Ppensar
from sqlalchemy.orm import Session
from typing import Union
from auth.jwt_bearer import JwtBearer
from fastapi import HTTPException, status

router_pensar = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_pensar.get("/tests", dependencies=[Depends(JwtBearer())] )
async def tests(code: int, current_year: int, state: str = None, db: Session = Depends(get_db)):
    test = Ppensar().get_tests(code, current_year, state, db)
    return test

@router_pensar.get("/tasks", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Tasks not found"},
    500: {"description": "Internal Server Error"}
})
async def task(db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(db)
    
    if not tasks:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer())])
async def results(db: Session = Depends(get_db)):
    results = Ppensar().global_results(db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer())])
async def component(db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(db)
    return cycle_results

@router_pensar.get("/components", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def components(codigoColegio: int = None,
                    grado: int = None, 
                    salon: str = None, 
                    idComponente: str = None, 
                    idArea: int = None,
                    db: Session = Depends(get_db)):
    _componentes = Ppensar().calculate_componentes(codigoColegio, grado, salon, idComponente, idArea, db)
    return _componentes


@router_pensar.get("/competencies", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def competencies(codigoColegio: int = None,
                    grado: int = None, 
                    salon: str = None, 
                    idCompetencia: int = None, 
                    idArea: int = None,
                    db: Session = Depends(get_db)):
    _competencia = Ppensar().calculate_competencias(codigoColegio, grado, salon, idCompetencia, idArea, db)
    if not _competencia:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Component not found")
    return _competencia

@router_pensar.get("/area", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Area not found"},
            500: {"description": "Internal Server Error"}
        })
async def area(codigoColegio: int, anio: int, 
               idPrueba: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grado: Union[int, None] = None, 
               salon: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _area = Ppensar().calculate_area(codigoColegio, anio, idPrueba, idArea, grado, salon, db)
    if not _area:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return _area


@router_pensar.get("/grado", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Grade not found"},
            500: {"description": "Internal Server Error"}
        })
async def grado(codigoColegio: int, anio: int,
               idPrueba: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grado: Union[int, None] = None, 
               salon: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _grado = Ppensar().calculate_grado(codigoColegio, anio, idPrueba, idArea, grado, salon, db)
    if not _grado:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return _grado

@router_pensar.get("/students", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Grade not found"},
            500: {"description": "Internal Server Error"}
        })
async def student(codigoColegio: int, anio: int,
               idPrueba: Union[int, None] = None,  
               db: Session = Depends(get_db)):
    
    _prueba_students = Ppensar().calculate_prueba_estudiantes(codigoColegio, anio, idPrueba, db)
    if not _prueba_students:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Students not found")
    return _prueba_students
    