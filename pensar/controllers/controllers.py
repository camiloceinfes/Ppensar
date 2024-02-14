from app.pensar.services.servicePensar import pensar as pns
from fastapi import APIRouter, HTTPException, Path
from app.config.db import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
from typing import Optional

router_pensar = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class parametros():
#     pass

@router_pensar.get("/componente")
async def component(grado: int, salon: str = None, area: str = None, comp: str = None, db: Session = Depends(get_db)):
    pensar = pns().componentes(grado, salon, area, comp, db)
    return pensar