from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# load_dotenv(".env")

#DB_HOST = "127.0.0.1:5432"
#DB_NAME = "Ppensar"
#DB_USER = "postgres"
#DB_PASSWORD = "950221"
#
#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

DB_HOST = "172.16.1.125:5432"
DB_NAME = "bd_eligetuu"
DB_USER = "usr_administrador"
DB_PASSWORD = "Ceinfe$2020"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()