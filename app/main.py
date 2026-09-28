from fastapi import FastAPI

from app.routers import applications, auth, companies, drives, students


app = FastAPI(
    title="Placement Management System API",
    description="Backend API for managing students and placements",
    version="0.1.0",
)


app.include_router(students.router)
app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(drives.router)
app.include_router(applications.router)


@app.get("/")
async def read_root():
    return {"message": "Placement Management System API"}