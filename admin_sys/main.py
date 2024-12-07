from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import uuid4

app = FastAPI()


# Pydantic model for teacher
class Teacher(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique Teacher ID"
    )
    name: str = Field(..., max_length=100, description="Full Name of the Teacher")
    email: EmailStr
    subject: str = Field(
        ..., max_length=50, description="Subject Taught by the Teacher"
    )
    phone: Optional[str] = Field(
        None, max_length=15, description="Teacher Phone Number"
    )
    is_active: bool = Field(default=True, description="Status of the Teacher")


# In-memory database
teachers_db: List[Teacher] = []


@app.post("/teachers/", response_model=Teacher, status_code=201)
def add_teacher(teacher: Teacher):
    """Add a new teacher to the database."""
    # Check if email already exists
    if any(t.email == teacher.email for t in teachers_db):
        raise HTTPException(
            status_code=400, detail="A teacher with this email already exists."
        )
    teachers_db.append(teacher)
    return teacher


@app.get("/teachers/", response_model=List[Teacher])
def list_teachers(
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get a list of all teachers, with optional filtering."""
    if is_active is not None:
        return [teacher for teacher in teachers_db if teacher.is_active == is_active]
    return teachers_db


@app.get("/teachers/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: str):
    """Get details of a specific teacher by ID."""
    for teacher in teachers_db:
        if teacher.id == teacher_id:
            return teacher
    raise HTTPException(status_code=404, detail="Teacher not found")


@app.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: str, updated_teacher: Teacher):
    """Update details of an existing teacher."""
    for index, teacher in enumerate(teachers_db):
        if teacher.id == teacher_id:
            teachers_db[index] = updated_teacher
            return updated_teacher
    raise HTTPException(status_code=404, detail="Teacher not found")


@app.delete("/teachers/{teacher_id}", response_model=dict)
def delete_teacher(teacher_id: str):
    """Delete a teacher record."""
    for index, teacher in enumerate(teachers_db):
        if teacher.id == teacher_id:
            del teachers_db[index]
            return {"message": "Teacher deleted successfully"}
    raise HTTPException(status_code=404, detail="Teacher not found")
