from fastapi import FastAPI,Depends,HTTPException
from Database import Base,engine,SessionLocal
import models
from pydantic import BaseModel,Field
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos,Users

app = FastAPI()

models.Base.metadata.create_all(bind = engine)


app = FastAPI()

class TodoRequest(BaseModel):
    title : str = Field(min_length= 1,max_length=1000)
    description : str = Field(min_length= 1,max_length=1000)
    priority : int = Field(gt=0,lt=6)
    complete : bool = Field(default=False)

class UserRequest(BaseModel):
    id : int = Field(gt = 0)
    email : str = Field(min_length=1,max_length=1000)
    username : str = Field(min_length=1,max_length=1000)
    first_name : str = Field(min_length=1,max_length=1000)
    last_name : str = Field(min_length=1,max_length=1000)
    hashed_password : str = Field(min_length=1,max_length=1000)
    is_active : bool = Field(default = True)
    role : str = Field(min_length=1,max_length=1000)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get('/all_books')
async def all_books(db : db_dependency):
    return db.query(Todos).all()

@app.get('/books/{title}')
async def book_by_title(db : db_dependency,title):
    todo_model = db.query(Todos).filter(Todos.title == title).all()
    if todo_model is None:
        raise HTTPException(status_code=404,details = 'Item Not found')
    return todo_model

@app.post('/books/post')
async def create_book(db : db_dependency,new_todo : TodoRequest):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()

@app.put('/update_todo/{todo_id}')
async def update_todo(db : db_dependency,update_todo : TodoRequest,todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code= 404,detail= 'Todo Not Found')
    todo_model.title = update_todo.title
    todo_model.description = update_todo.description
    todo_model.priority = update_todo.priority
    todo_model.complete = update_todo.complete

    db.add(todo_model)
    db.commit()

@app.delete('/delete_todo/{todo_id}')
async def delete_todo(db : db_dependency,todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code= 404, detail= "Item Not Found")
    db.delete(todo_model)
    db.commit()


@app.get('/all_users')
async def all_users(db : db_dependency):
    return db.query(Users).all()

@app.post('/create_user')
async def create_user(db : db_dependency,user_request : UserRequest):
    users = Users(**user_request.model_dump())
    db.add(users)
    db.commit()
