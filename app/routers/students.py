from fastapi import FastAPI ,HTTPException , APIRouter
from pydantic import BaseModel
from typing import Annotated

router=APIRouter(prefix='/students' , tags=['Students'])


class NewStudent(BaseModel):
    name:str
    class_no:int


students_db : list[dict]=[{'id' : 1 , 'name':'ravi' , 'class_no' :10}]

def not_found(m):
    raise HTTPException(status_code=404 , detail=m)

@router.get('/')
async def get_students(classno : Annotated[int | None , ' get students by class'] = None):
    if classno is not None :
        temp=[]
        for student in students_db :
            if classno == student['class_no']:
                temp.append(student)
        if not temp:
            not_found('Students not found')
        return temp

    return students_db

@router.get('/{id}')
async def get_student_by_id(id:int ):
    for student in students_db:
        if student['id']==id:
            return student
    not_found('student not found')

@router.post('/')
async def create_student(student : NewStudent):
    id= students_db[-1]['id']+1 if students_db else 1
    new_entry = {'id':id , 'name' : student.name , 'class_no': student.class_no}
    students_db.append(new_entry)
    return new_entry

@router.put('/{id}')
async def update_student(id:int ,student : NewStudent) :
    for db_student in students_db :
        if id == db_student['id']:
            db_student.update({'name': student.name , 'class_no' : student.class_no})
            return db_student
    not_found('student not found')

@router.delete('/{id}')
async def delete_student(id:int):
    for student in students_db:
        if id ==student['id']:
            
            students_db.remove(student)
            return student
    not_found('student not found')