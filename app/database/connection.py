import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

student_db = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"))


if __name__ == '__main__' :
    print("✅ Connected Successfully!")
    curr =student_db.cursor(row_factory=dict_row)
    curr.execute('SELECT * FROM students ')
    print(curr.fetchall())

    # curr.execute("INSERT INTO students(name ,class_no) Values (  %(name)s , %(class_no)s)" ,
    #               { 'name' : 'Guna' , 'class_no' :12 })

    # student_db.commit()
    # curr.execute("DROP TABLE students;")
    # student_db.commit()
  

#     curr.execute("""
#     INSERT INTO students (name, class_no)
#       VALUES
#     ('Ravi', 10),
#     ('Ram', 9),
#     ('Arun', 7),
#     ('Guna', 12),
#     ('Sujan', 12);
#     """)

    student_db.commit()


    curr.close()

    student_db.close()