from fastapi import FastAPI
from app.routes.availability import router as availability_router
from app.routes.booking import router as booking_router
from app.routes.subject import router as subject_router
from app.routes.student import router as student_router

app = FastAPI(
    title="Scheduling System",
    description="API for managing tutor availability and student bookings",
    version="1.0.0"
)

# Include API routers
app.include_router(availability_router, prefix="/api")
app.include_router(booking_router, prefix="/api")
app.include_router(subject_router, prefix="/api")
app.include_router(student_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Scheduling System API"}
