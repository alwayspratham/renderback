from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv
import os

load_dotenv()

DATABASEURL = os.getenv("DATABASEURL")
DATABASEURL=os.getenv("DATABASEURL")

engine=create_engine(
    DATABASEURL,
    pool_pre_ping=True

)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()