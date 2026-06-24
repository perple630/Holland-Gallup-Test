from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db
from app.services import user_service

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


@router.get("/students", response_model=List[schemas.StudentListItem])
def list_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    return user_service.list_students(db)


@router.post("/students", response_model=schemas.UserOut)
def create_student(
    body: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    password = body.password or user_service.generate_temp_password()
    user = user_service.create_user(
        db,
        username=body.username,
        password=password,
        role=models.UserRole.student,
        display_name=body.display_name or body.username,
        email=body.email,
        grade=body.grade,
        class_name=body.class_name,
        school=body.school,
        phone=body.phone,
        created_by=current_user.id,
        must_change_password=True,
    )
    return user_service.user_to_out(user)


@router.patch("/students/{student_id}", response_model=schemas.UserOut)
def update_student(
    student_id: str,
    body: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    student = db.query(models.User).filter(
        models.User.id == student_id,
        models.User.role == models.UserRole.student,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    user = user_service.update_profile(db, student, body)
    return user_service.user_to_out(user)


@router.post("/students/{student_id}/reset-password", response_model=schemas.ResetPasswordResponse)
def reset_student_password(
    student_id: str,
    body: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    student = db.query(models.User).filter(
        models.User.id == student_id,
        models.User.role == models.UserRole.student,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    new_password = body.new_password or user_service.generate_temp_password()
    user_service.validate_password(new_password)
    student.password_hash = auth.get_password_hash(new_password)
    student.must_change_password = True
    db.commit()
    return schemas.ResetPasswordResponse(
        username=student.username,
        new_password=new_password,
        must_change_password=True,
    )


@router.post("/students/{student_id}/deactivate")
def deactivate_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    student = db.query(models.User).filter(
        models.User.id == student_id,
        models.User.role == models.UserRole.student,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    student.is_active = False
    db.commit()
    return {"message": "学生账号已停用"}


@router.post("/students/{student_id}/activate")
def activate_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_teacher),
):
    student = db.query(models.User).filter(
        models.User.id == student_id,
        models.User.role == models.UserRole.student,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    student.is_active = True
    db.commit()
    return {"message": "学生账号已启用"}
