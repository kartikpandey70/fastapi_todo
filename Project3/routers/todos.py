from fastapi import FastAPI,Depends
from pydantic import BaseModel,Field
from Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos


app = FastAPI()

class TodoRequest(BaseModel):
    title : str = Field(min_length= 1,max_length=1000)
    description : str = Field(min_length= 1,max_length=1000)
    priority : int = Field(gt=0,lt=6)
    complete : bool = Field(default=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get('/all_books')
def all_books(db : db_dependency):
    return db.query(Todos).all()