from fastapi import FastAPI
from config.db import Base, engine
from pensar.controllers.controllers import router_pensar
import pensar.models.models as pen
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#pen.Base.metadata.create_all(bind=engine)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(router_pensar, prefix="/api/pensar", tags=["Pensar"])