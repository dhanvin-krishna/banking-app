from fastapi import FastAPI
from database import engine, Base
import models.users
from routers.auth import router as auth_router



app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)

@app.get("/")

def root():
    return {"message": "Welcome to the Banking API"}
