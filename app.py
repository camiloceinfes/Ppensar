from fastapi import FastAPI
from app.config.db import Base, engine
from app.pensar.controllers.controllers import router_pensar
import app.pensar.models.models as pen

app = FastAPI()

pen.Base.metadata.create_all(bind=engine)

app.include_router(router_pensar, prefix="/Pruebapensar", tags=["componente"])