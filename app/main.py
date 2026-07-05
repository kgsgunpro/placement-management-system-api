from fastapi import FastAPI
from app.routers import students
app = FastAPI()
app.include_router(students.router)

@app.get("/")
async def read_root() :
    return {"Hello": "World"}