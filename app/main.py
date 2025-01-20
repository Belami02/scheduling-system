from fastapi import FastAPI
from app.routes.availability import router as availability_router
from app.routes.booking import router as booking_router

app = FastAPI()

app.include_router(availability_router, prefix="/api")
app.include_router(booking_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Scheduling System"}
