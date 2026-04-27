from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

from Backend.db.session import get_db
from Backend.db.database import Base, engine
from Backend.routes import auth, task

Base.metadata.create_all(bind=engine)

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def db_conncetion(db:Session=Depends(get_db)):
    return {"message":"Conncetion is eshtablished"}