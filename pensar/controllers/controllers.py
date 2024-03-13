from auth.role import RoleChecker
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
@router_pensar.get("/global-params", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Resource not found"},
    500: {"description": "Internal Server Error"}
})
async def global_params(code: int, year: int, db: Session = Depends(get_db)):
    global_params = Ppensar().get_global_params(code, year, db)
    
    if not global_params:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return global_params

@router_pensar.get("/tests",
                   dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], 
                   responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
} )
async def tests(code: int, year: int, idTest:int = None, db: Session = Depends(get_db)):
    test = Ppensar().get_tests(code, year, idTest, db)
    return test

@router_pensar.get("/tasks", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Tasks not found"},
    500: {"description": "Internal Server Error"}
})
async def task(code: int, year: int,  idGrade: int = None, idClassroom: int = None, idPrueba: int = None, idArea: int = None, db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(code, year, idGrade, idClassroom, idPrueba, idArea, db)
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Results not found"},
    500: {"description": "Internal Server Error"}
})
async def results(code: int, year: int, idPrueba:int = None, db: Session = Depends(get_db)):
    results = Ppensar().global_results(code, year, idPrueba, db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Results not found"},
    500: {"description": "Internal Server Error"}
})
async def cycle_results(code: int, year: int, idPrueba:int = None, db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(code, year, idPrueba, db)
    return cycle_results

@router_pensar.get("/components", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def components(codigoColegio: int, anio: int, 
                    grado: Union[int, None] = None, 
                    salon: Union[str, None] = None, 
                    idComponente: Union[int, None] = None, 
                    idArea: Union[int, None] = None, 
                    db: Session = Depends(get_db)):
    
    grado = grado or 0    
    salon = salon or 0
    idComponente = idComponente or 0
    idArea = idArea or 0

    _componentes = Ppensar().calculate_componentes(codigoColegio, anio, grado, salon, idComponente, idArea, db)
    # if not _competencia:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencie not found")
    return _componentes


@router_pensar.get("/competencies", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def competencies(codigoColegio: int, anio: int, 
                    grado: Union[int, None] = None, 
                    salon: Union[str, None] = None, 
                    idCompetencia: Union[int, None] = None, 
                    idArea: Union[int, None] = None, 
                    db: Session = Depends(get_db)):
    
    grado = grado or 0 
    salon = salon or 0
    idCompetencia = idCompetencia or 0
    idArea = idArea or 0

    _competencia = Ppensar().calculate_competencias(codigoColegio, anio, grado, salon, idCompetencia, idArea, db)
    # if not _competencia:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencie not found")
    return _competencia

@router_pensar.get("/area", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def area(codigoColegio: int, anio: int, 
               idComponente: Union[int, None] = None, 
               idPrueba: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grado: Union[int, None] = None, 
               salon: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    idPrueba = idPrueba or -1
    idArea   = idArea or -1
    grado    = grado or -1
    salon    = salon or -1

    _area = Ppensar().calculate_area(codigoColegio, anio, idComponente, idPrueba, idArea, grado, salon, db)
    if not _area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _area

@router_pensar.get("/grado", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def grado(codigoColegio: int, anio: int,
               idComponente: Union[int, None] = None,
               idPrueba: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grado: Union[int, None] = None, 
               salon: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    idPrueba = idPrueba or -1
    idArea   = idArea or -1
    grado    = grado or -1
    salon    = salon or -1
    
    _grado = Ppensar().calculate_grado(codigoColegio, anio, idComponente, idPrueba, idArea, grado, salon, db)
    if not _grado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _grado

@router_pensar.get("/students", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def student(codigoColegio: int, anio: int, grado: int,
                salon: Union[int, None] = None,
                idPrueba: Union[int, None] = None, 
                db: Session = Depends(get_db)):
    
    grado = idPrueba or -1
    idPrueba = idPrueba or -1
    salon    = salon or -1

    _student = Ppensar().calculate_prueba_estudiantes(codigoColegio, anio, idPrueba, grado, salon, db)
    if not _student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _student

@router_pensar.get("/students/tasks", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Resource not found"},
    500: {"description": "Internal Server Error"}
})
async def tasks_students(code: int, year: int, idGrade: int, idArea: int, taskName: str, classroom: int = None, idPrueba: int = None, db: Session = Depends(get_db)):
    tasks_students = Ppensar().students_tasks(code, year, idGrade, classroom, idPrueba, idArea, taskName, db)
    return tasks_students

@router_pensar.get("/detail", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))])
async def detail(codigoColegio: int, anio: int,
                 grado: int, idPrueba: int,
                 idArea: Union[int, None] = None,
                 db: Session = Depends(get_db)):
    
    idArea = idArea or 0
    _detail = Ppensar().detail_test(codigoColegio, anio, grado, idArea, idPrueba, db)
    # if not _student:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return _detail

@router_pensar.get("/level-performance", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))],responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def level_performance(codigoColegio: int, 
                            anio: int, 
                            grado: int,
                salon: Union[int, None] = None,
                idPrueba: Union[int, None] = None, 
                db: Session = Depends(get_db)):
    
    grado = idPrueba or -1
    idPrueba = idPrueba or -1
    salon    = salon or -1
    _performance = Ppensar().performance(codigoColegio, anio, grado, salon, idPrueba, db)
    if not _performance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _performance
