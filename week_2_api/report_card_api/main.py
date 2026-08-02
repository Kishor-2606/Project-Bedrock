from fastapi import FastAPI, status

from student import Student
from schemas import StudentRequest, StudentResponse

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Student Report Card API"}


@app.post(
    "/report",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_report(student: StudentRequest):

    student_obj = Student(
        student.student_id,
        student.student_name,
        student.subject_marks
    )

    report = student_obj.generate_report()

    return report