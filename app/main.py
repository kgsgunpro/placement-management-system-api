from fastapi import FastAPI
from app.routers import students


app = FastAPI( title="Placement Management System API",
    description="Backend API for managing students and placements",
    version="0.1.0")


app.include_router(students.router)

@app.get("/")
async def read_root() :
    return {"Hello": "World"}