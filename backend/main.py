from fastapi import FastAPI
from database import engine, Base
import models.users


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")

def root():
    return {"message": "Welcome to the Banking API"}
