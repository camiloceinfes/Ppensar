from fastapi import FastAPI
from config.db import Base, engine
from pensar.controllers.controllers import router_pensar
import pensar.models.models as pen

app = FastAPI()

pen.Base.metadata.create_all(bind=engine)

app.include_router(router_pensar, prefix="/Pruebapensar", tags=["componente"])