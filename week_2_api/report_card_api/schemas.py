from pydantic import BaseModel, Field,field_validator

class StudentRequest(BaseModel):
    student_id: int = Field(gt=0)
    student_name: str = Field(min_length=1, max_length=50)
    subject_marks: dict[str, int]

    @field_validator("subject_marks")
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise ValueError("subject_marks cannot be empty")
        return v


class StudentResponse(BaseModel):
    student_id: int
    student_name: str
    average: float
    grade: str