"""
Main module for the Scheduling System API.
"""

from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Scheduling System API"}
