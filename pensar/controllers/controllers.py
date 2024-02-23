from pensar.services.servicePensar import pensar as pns
from fastapi import APIRouter, HTTPException, Path
from config.db import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
from typing import Optional
from pensar.repository import pensar

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
    test = pensar.get_tests(code,current_year,state,db)
    return test

@router_pensar.get("/tasks")
async def test(grado: int, salon: str = None, area: str = None,  db: Session = Depends(get_db)):
    tasks = pensar.get_tasks(grado,salon, area,db)
    return tasks

@router_pensar.get("/results")
async def results(db: Session = Depends(get_db)):
    results = pensar.global_results(db)
    return results

@router_pensar.get("/cycle/results")
async def component(db: Session = Depends(get_db)):
    cycle_results = pensar.cycle_results(db)
    return cycle_results

@router_pensar.get("/components")
async def component(grado: int, salon: str = None, area: str = None, comp: str = None, db: Session = Depends(get_db)):
    pensar = pns().componentes(grado, salon, area, comp, db)
    return pensar

@router_pensar.get("/competences/{idColegio}")
async def competencies(idColegio: int, db: Session = Depends(get_db)):
    _competencias = pns().competencias(idColegio, db)
    return _competencias