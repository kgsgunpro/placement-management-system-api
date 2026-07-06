from fastapi import FastAPI ,HTTPException , APIRouter
from pydantic import BaseModel

router=APIRouter(prefix='/students' , tags=['Students'])


class NewStudent(BaseModel):    
    name:str
    class_no:int


students_db=[{'id' : 1 , 'name':'ravi' , 'class_no' :10}]



@router.get('/')
async def get_students():
    return students_db

@router.get('/{id}')
async def get_student_by_id(id:int):
    for student in students_db:
        if student['id']==id:
            return student
    raise HTTPException(status_code=404 , detail='student not found')

@router.post('/')
async def create_student(student : NewStudent):
    id= students_db[-1]['id']+1 if students_db else 1
    new_entry = {'id':id , 'name' : student.name , 'class_no': student.class_no}
    students_db.append(new_entry)
    return new_entry

@router.put('/{id}')
async def update_student(id:int ,student : NewStudent) :
    for students in students_db :
        if id == students['id']:
            students.update({'name': student.name , 'class' : student.class_no})
            return students
    return HTTPException(status_code=404 , detail = 'Student not found')

@router.delete('/{id}')
async def delete_student(id:int):
    for students in students_db:
        if id ==students['id']:
            temp=students
            students_db.remove(students)
            return temp
    return HTTPException(status_code=404 , detail='Student not found')