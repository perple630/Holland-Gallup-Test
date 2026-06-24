"""用户创建、资料完善与列表查询。"""
from __future__ import annotations

import re
import secrets
import string
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import auth, models, schemas

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]).{8,}$"
)


def validate_password(password: str):
    if not PASSWORD_PATTERN.match(password):
        raise HTTPException(
            status_code=400,
            detail="密码至少 8 位，且需包含大小写字母、数字和特殊字符",
        )


def generate_temp_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if PASSWORD_PATTERN.match(pwd):
            return pwd


def compute_profile_complete(user: models.User) -> bool:
    return bool(
        (user.display_name or "").strip()
        and (user.school or "").strip()
        and (user.grade or "").strip()
    )


def refresh_profile_complete(user: models.User):
    user.profile_complete = compute_profile_complete(user)


def user_to_out(user: models.User) -> schemas.UserOut:
    return schemas.UserOut(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        role=user.role,
        email=user.email,
        grade=user.grade,
        class_name=user.class_name,
        school=user.school,
        phone=user.phone,
        career_note=user.career_note,
        profile_complete=bool(user.profile_complete),
        must_change_password=bool(user.must_change_password),
        is_active=bool(user.is_active),
        created_at=user.created_at,
    )


def create_user(
    db: Session,
    *,
    username: str,
    password: str,
    role: models.UserRole,
    display_name: Optional[str] = None,
    email: Optional[str] = None,
    grade: Optional[str] = None,
    class_name: Optional[str] = None,
    school: Optional[str] = None,
    phone: Optional[str] = None,
    created_by: Optional[str] = None,
    must_change_password: bool = False,
) -> models.User:
    username = username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="用户名不能为空")
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    validate_password(password)

    user = models.User(
        username=username,
        display_name=display_name or username,
        role=role,
        password_hash=auth.get_password_hash(password),
        email=email,
        grade=grade,
        class_name=class_name,
        school=school,
        phone=phone,
        created_by=created_by,
        must_change_password=must_change_password,
        is_active=True,
    )
    refresh_profile_complete(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    auth.get_or_create_assessment(db, user.id)
    return user


def update_profile(db: Session, user: models.User, data: schemas.ProfileUpdate) -> models.User:
    for field in ("display_name", "email", "grade", "class_name", "school", "phone", "career_note"):
        value = getattr(data, field)
        if value is not None:
            setattr(user, field, value.strip() if isinstance(value, str) else value)
    refresh_profile_complete(user)
    db.commit()
    db.refresh(user)
    return user


def student_list_item(db: Session, student: models.User) -> schemas.StudentListItem:
    assessment = db.query(models.AssessmentStatus).filter(
        models.AssessmentStatus.user_id == student.id
    ).first()
    return schemas.StudentListItem(
        id=student.id,
        username=student.username,
        display_name=student.display_name,
        email=student.email,
        grade=student.grade,
        class_name=student.class_name,
        school=student.school,
        phone=student.phone,
        profile_complete=bool(student.profile_complete),
        is_active=bool(student.is_active),
        holland_done=bool(assessment.holland_done) if assessment else False,
        gallup_done=bool(assessment.gallup_done) if assessment else False,
        holland_code=assessment.holland_code if assessment else None,
        gallup_domain=assessment.gallup_domain if assessment else None,
        gallup_secondary_domain=assessment.gallup_secondary_domain if assessment else None,
    )


def list_students(db: Session) -> List[schemas.StudentListItem]:
    students = (
        db.query(models.User)
        .filter(models.User.role == models.UserRole.student)
        .order_by(models.User.created_at.desc())
        .all()
    )
    return [student_list_item(db, s) for s in students]
