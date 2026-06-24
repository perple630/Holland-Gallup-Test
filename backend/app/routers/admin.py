from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, auth
from app.database import get_db
from app.services import user_service

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=schemas.PlatformStats)
def platform_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin),
):
    users = db.query(models.User).all()
    assessments = db.query(models.AssessmentStatus).all()
    return schemas.PlatformStats(
        total_users=len(users),
        students=sum(1 for u in users if u.role == models.UserRole.student),
        teachers=sum(1 for u in users if u.role == models.UserRole.teacher),
        admins=sum(1 for u in users if u.role == models.UserRole.admin),
        completed_assessments=sum(
            1 for a in assessments if a.holland_done and a.gallup_done
        ),
        holland_completed=sum(1 for a in assessments if a.holland_done),
        gallup_completed=sum(1 for a in assessments if a.gallup_done),
    )


@router.get("/users", response_model=List[schemas.UserOut])
def list_users(
    role: Optional[models.UserRole] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin),
):
    q = db.query(models.User).order_by(models.User.created_at.desc())
    if role:
        q = q.filter(models.User.role == role)
    return [user_service.user_to_out(u) for u in q.all()]


@router.post("/users", response_model=schemas.UserOut)
def create_user(
    body: schemas.AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin),
):
    if body.role == models.UserRole.admin and current_user.username != "admin":
        raise HTTPException(status_code=403, detail="仅主管理员可创建管理员账号")
    password = body.password or user_service.generate_temp_password()
    user = user_service.create_user(
        db,
        username=body.username,
        password=password,
        role=body.role,
        display_name=body.display_name or body.username,
        email=body.email,
        grade=body.grade,
        class_name=body.class_name,
        school=body.school,
        phone=body.phone,
        created_by=current_user.id,
        must_change_password=body.role != models.UserRole.student,
    )
    return user_service.user_to_out(user)


@router.patch("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: str,
    body: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if body.role and body.role == models.UserRole.admin and user.id != current_user.id:
        if current_user.username != "admin":
            raise HTTPException(status_code=403, detail="仅主管理员可调整管理员角色")
        user.role = body.role
    elif body.role:
        user.role = body.role
    profile_fields = schemas.ProfileUpdate(
        display_name=body.display_name,
        email=body.email,
        grade=body.grade,
        class_name=body.class_name,
        school=body.school,
        phone=body.phone,
        career_note=body.career_note,
    )
    user_service.update_profile(db, user, profile_fields)
    if body.is_active is not None:
        user.is_active = body.is_active
        db.commit()
        db.refresh(user)
    return user_service.user_to_out(user)


@router.post("/users/{user_id}/reset-password", response_model=schemas.ResetPasswordResponse)
def reset_user_password(
    user_id: str,
    body: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    new_password = body.new_password or user_service.generate_temp_password()
    user_service.validate_password(new_password)
    user.password_hash = auth.get_password_hash(new_password)
    user.must_change_password = True
    db.commit()
    return schemas.ResetPasswordResponse(
        username=user.username,
        new_password=new_password,
        must_change_password=True,
    )
