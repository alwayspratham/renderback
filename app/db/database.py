from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASEURL="mysql+pymysql://root:pratham123@localhost/intern_project"

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