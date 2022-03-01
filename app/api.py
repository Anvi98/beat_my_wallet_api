from fastapi import FastAPI, Path
from typing import Optional
from . import schemas

app = FastAPI()

students = {
  1: {
        "name":"john",
        "age":17,
        "year": "year 12"
  }
}


@app.get("/")
def index():
  return {"name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description=" The ID of the student you want to view")):
  return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None):
  for student_id in students:
    if students[student_id]["name"] == name:
      return students[student_id]
  return {"Data": "Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: schemas.Student):
  if(student_id in students):
    return {"Error": "Student already exists"}
  
  students[student_id] = student
  return student_id

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: schemas.UpdateStudent):
  if student_id not in students:
    return {"Error-404": "Student not exists yet"}
  
  if student.name != None:
    students[student_id].name = student.name

  if student.age != None:
    students[student_id].age = student.age
  
  if student.year != None:
    students[student_id].year = student.year

  return student_id

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
  if student_id not in students:
    return {"Error-404": "Data not found"}
  del students[student_id]
  return {"Message": "Student deleted successfully"}