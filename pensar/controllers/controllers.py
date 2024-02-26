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
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer())])
async def results(code: int, year: int, idPrueba:int = None, db: Session = Depends(get_db)):
    results = Ppensar().global_results(code, year, idPrueba, db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer())])
async def component(db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(db)
    return cycle_results

@router_pensar.get("/componentes", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def component(codigoColegio: int,
                    grado: int, 
                    salon: str = None, 
                    idComponente: str = None, 
                    idArea: int = None,
                    db: Session = Depends(get_db)):
    _componentes = Ppensar().calculate_componentes(codigoColegio, grado, salon, idComponente, idArea, db)
    if not _componentes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
    return _componentes


@router_pensar.get("/competencias", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def component(codigoColegio: int,
                    grado: int, 
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