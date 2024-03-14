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
async def task(code: int, year: int,  idGrade: int = None, idClassroom: int = None, idTest: int = None, idArea: int = None, db: Session = Depends(get_db)):
    tasks = Ppensar().get_tasks(code, year, idGrade, idClassroom, idTest, idArea, db)
    return tasks

@router_pensar.get("/results", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Results not found"},
    500: {"description": "Internal Server Error"}
})
async def results(code: int, year: int, idTest:int = None, db: Session = Depends(get_db)):
    results = Ppensar().global_results(code, year, idTest, db)
    return results

@router_pensar.get("/cycle/results", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Results not found"},
    500: {"description": "Internal Server Error"}
})
async def cycle_results(code: int, year: int, idTest:int = None, db: Session = Depends(get_db)):
    cycle_results = Ppensar().cycle_results(code, year, idTest, db)
    return cycle_results

@router_pensar.get("/components", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
            200: {"description": "Successful Response"},
            404: {"description": "Tasks not found"},
            500: {"description": "Internal Server Error"}
        })
async def components(code: int, year: int, 
                    grade: Union[int, None] = None, 
                    classroom: Union[int, None] = None, 
                    idComponent: Union[int, None] = None, 
                    idArea: Union[int, None] = None, 
                    db: Session = Depends(get_db)):
    
    _componentes = Ppensar().components_calculate(code, year, grade, classroom, idComponent, idArea, db)
    # if not _competencia:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencie not found")
    return _componentes


@router_pensar.get("/competencies", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def competences(code: int, year: int, 
                    grade: Union[int, None] = None, 
                    classroom: Union[str, None] = None, 
                    idCompetence: Union[int, None] = None, 
                    idArea: Union[int, None] = None, 
                    db: Session = Depends(get_db)):
    
    _competencia = Ppensar().competences_calculate(code, year, grade, classroom, idCompetence, idArea, db)
    # if not _competencia:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencie not found")
    return _competencia

@router_pensar.get("/area", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def area(code: int, year: int,
               idTest: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grade: Union[int, None] = None, 
               classroom: Union[int, None] = None, 
               db: Session = Depends(get_db)):
    
    _area = Ppensar().area_calculate(code, year, idTest, idArea, grade, classroom, db)
    if not _area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _area

@router_pensar.get("/grado", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def grade(code: int, year: int,
               idTest: Union[int, None] = None, 
               idArea: Union[int, None] = None, 
               grade: Union[int, None] = None, 
               classroom: Union[int, None] = None, 
               db: Session = Depends(get_db)):
        
    _grado = Ppensar().grade_calculate(code, year, idTest, idArea, grade, classroom, db)
    if not _grado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _grado

@router_pensar.get("/students", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def student(code: int, year: int, grade: int,
                classroom: Union[int, None] = None,
                idTest: Union[int, None] = None, 
                db: Session = Depends(get_db)):
    
    _student = Ppensar().students_test_calculate(code, year, idTest, grade, classroom, db)
    if not _student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _student

@router_pensar.get("/students/tasks", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Successful Response"},
    404: {"description": "Resource not found"},
    500: {"description": "Internal Server Error"}
})
async def tasks_students(code: int, year: int, idGrade: int, idArea: int, taskName: str, classroom: int = None, idTest: int = None, db: Session = Depends(get_db)):
    tasks_students = Ppensar().students_tasks(code, year, idGrade, classroom, idTest, idArea, taskName, db)
    return tasks_students

@router_pensar.get("/detail", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))])
async def detail(code: int, year: int,
                 grade: int, idTest: int,
                 idArea: Union[int, None] = None,
                 db: Session = Depends(get_db)):
    
    idArea = idArea or 0
    _detail = Ppensar().detail_test(code, year, grade, idArea, idTest, db)
    # if not _student:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return _detail

@router_pensar.get("/level-performance", dependencies=[Depends(JwtBearer()), Depends(RoleChecker(allowed_roles=["DIR_INS"]))],responses={   
                    200: {"description": "Successful Response"},
                    404: {"description": "Resource not found"},
                    500: {"description": "Internal Server Error"}
                })
async def level_performance(code: int, 
                            year: int, 
                            idTest: int, 
                            classroom: Union[int, None] = None,
                            grade: Union[int, None] = None,
                            db: Session = Depends(get_db)):
    
    _performance = Ppensar().performance(code, year, grade, classroom, idTest, db)
    if not _performance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return _performance
