from dotenv import load_dotenv
from db.models.users import User
from sqlmodel import SQLModel, Session, create_engine
import os

load_dotenv()

# Carga de .env
URL = os.getenv("URL")

# Configurar la conexión a la base de datos PostgreSQL
engine = create_engine(URL, echo=True)

session = Session(engine)
