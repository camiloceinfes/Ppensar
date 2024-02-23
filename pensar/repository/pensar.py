from sqlalchemy.orm import Session
from pensar.models import models

def get_tests(code, current_year, state, db: Session):
    pensar = db.query(models.Pensar).filter(models.Pensar.año_ciclo == current_year).all()
    print(pensar)
    if not pensar:
        return { 
            "status_code": "404",
            "message": "Resource not found" 
        }
    return pensar

def get_tasks(grado, salon, area, db: Session):
    return ''

def global_results(db: Session):
    return ''

def cycle_results(db: Session):
    return ''