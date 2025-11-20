from fastapi import FastAPI, Depends
from routers import student
from schema.users import User, UserCreate
from deps import init_db_connection, close_db_connection
from typing import Annotated
import auth
from auth import get_current_user, get_password_hash

app = FastAPI()

app.include_router(student.router)
app.include_router(auth.app)


@app.get("/")
def health():
    return {"health":"ok"}

@app.post("/signup")
def signup(user_data: UserCreate):
    conn, cur = init_db_connection()
    cur.execute("INSERT INTO users(full_name, email, hashed_password, role) VALUES(%s, %s, %s, %s)",(user_data.full_name, user_data.email, get_password_hash(user_data.password), user_data.role))
    conn.commit()
    close_db_connection(conn,cur)
    return {"message":"User Signup Successful","data":user_data}

@app.get("/me")
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return {"data":current_user}