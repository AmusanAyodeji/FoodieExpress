from fastapi import FastAPI, Depends
from routers import student
import auth
from routers import vendor

app = FastAPI()

app.include_router(auth.app, tags=["Authentication"])
app.include_router(student.student_router, tags=["Students"])
app.include_router(vendor.router, tags=["Vendors"])


@app.get("/")
def health():
    return {"health":"ok"}