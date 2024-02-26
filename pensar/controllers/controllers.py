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

@router_pensar.get("/components", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def components(codigoColegio: int,
                    grado: int, 
                    salon: str = None, 
                    idComponente: str = None, 
                    idArea: int = None,
                    db: Session = Depends(get_db)):
        
    salon = salon or 0
    idComponente = idComponente or 0
    idArea = idArea or 0

    _componentes = Ppensar().calculate_componentes(codigoColegio, grado, salon, idComponente, idArea, db)
    return _componentes


@router_pensar.get("/competencies", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def competencies(codigoColegio: int,
                    grado: int, 
                    salon: str = None, 
                    idCompetencia: int = None, 
                    idArea: int = None,
                    db: Session = Depends(get_db)):
        
    salon = salon or 0
    idCompetencia = idCompetencia or 0
    idArea = idArea or 0

    _competencia = Ppensar().calculate_competencias(codigoColegio, grado, salon, idCompetencia, idArea, db)
    return _competencia

@router_pensar.get("/area", dependencies=[Depends(JwtBearer())])
async def area(codigoColegio: int, anio: int, 
               idPrueba: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grado: Union[int, None] = None, 
               salon: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    idPrueba = idPrueba or -1
    idArea   = idArea or -1
    grado    = grado or -1
    salon    = salon or -1

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
    
    idPrueba = idPrueba or -1
    idArea   = idArea or -1
    grado    = grado or -1
    salon    = salon or -1
    
    _grado = Ppensar().calculate_grado(codigoColegio, anio, idPrueba, idArea, grado, salon, db)
    if not _grado:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return _grado

@router_pensar.get("/students", dependencies=[Depends(JwtBearer())])
async def student(codigoColegio: int, anio: int,
               idPrueba: Union[int, None] = None,  
               db: Session = Depends(get_db)):
    idPrueba = idPrueba or -1
    _student = Ppensar().calculate_prueba_estudiantes(codigoColegio, anio, idPrueba, db)
    
    return _student

@router_pensar.get("/students/tasks", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Resource not found"},
    500: {"description": "Internal Server Error"}
})
async def tasks_students(code: int, year: int, idGrade: int, idArea: int, classroom: int = None, idPrueba: int = None, taskName: str = None, db: Session = Depends(get_db)):
    tasks_students = Ppensar().students_tasks(code, year, idGrade, classroom, idPrueba, idArea, taskName, db)
    return tasks_students
