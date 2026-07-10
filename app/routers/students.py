from fastapi import FastAPI ,HTTPException , APIRouter
from pydantic import BaseModel
from typing import Annotated
from app.database.connection import student_db , dict_row

#postgreSQL

cur = student_db.cursor(row_factory=dict_row)



#router
router=APIRouter(prefix='/students' , tags=['Students'])


class NewStudent(BaseModel):
    name:str
    class_no:int



class Student(NewStudent):
    id :int


# students_db : list[dict]=[{'id' : 1 , 'name':'ravi' , 'class_no' :10}]

def not_found(m):
    raise HTTPException(status_code=404 , detail=m)


@router.get('/' , response_model=list[Student])
async def get_students(classno : Annotated[int | None , ' get students by class'] = None):
    if classno is not None :
        cur.execute('select * from students where class_no= %(class_no)s' , {'class_no' : classno})
        temp= cur.fetchall()
        if not temp:
            not_found('Students not found')
        return temp
    cur.execute('select * from students')
    temp=cur.fetchall()
    return temp

@router.get('/{id}' , response_model= Student )
async def get_student_by_id(id:int ):
    cur.execute('select * from students where id = %s' , (id ,))
    rows=cur.fetchall()
    if rows :
        return rows[0]
    not_found('student not found')

@router.post('/' , response_model=Student , status_code= 201)
async def create_student(student : NewStudent):
    new_entry = {'name' : student.name , 'class_no': student.class_no}
    cur.execute('''insert into students (  name , class_no ) 
                values ( %(name)s ,%(class_no)s  ) 
                returning * ;''' , new_entry )
    student_db.commit()
    new_entry = cur.fetchone()
    return new_entry

@router.put('/{id}' , response_model= Student ,status_code=200)
async def update_student(id:int ,student : NewStudent) :
    cur.execute('select * from students where id = %s' , (id,))
    rows=cur.fetchall()
    if rows:
        update_entry = { 'id' :id ,'name' : student.name , 'class_no' : student.class_no  }
        cur.execute('''update students
                        set name = %(name)s ,class_no= %(class_no)s 
                        where id=%(id)s  ; ''' , update_entry)
        student_db.commit()
        return update_entry
    not_found('student not found')

@router.delete('/{id}' , status_code=204)
async def delete_student(id:int):
    cur.execute('select * from students where id = %s' , (id,))
    rows=cur.fetchall()
    if rows:
        cur.execute('DELETE FROM students where id = %s' , (id,))
        student_db.commit()
        return
    not_found('student not found')