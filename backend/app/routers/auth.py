from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db
from app.services import user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut)
def register_student(user_in: schemas.StudentRegister, db: Session = Depends(get_db)):
    """学生自助注册。"""
    user = user_service.create_user(
        db,
        username=user_in.username,
        password=user_in.password,
        role=models.UserRole.student,
        display_name=user_in.display_name or user_in.username,
        email=user_in.email,
        grade=user_in.grade,
        class_name=user_in.class_name,
        school=user_in.school,
        phone=user_in.phone,
    )
    return user_service.user_to_out(user)


@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已停用，请联系管理员")
    return auth.build_token_response(user)


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(auth.get_current_user)):
    return user_service.user_to_out(current_user)


@router.patch("/profile", response_model=schemas.UserOut)
def update_profile(
    data: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    user = user_service.update_profile(db, current_user, data)
    return user_service.user_to_out(user)


@router.post("/change-password")
def change_password(
    body: schemas.ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if not auth.verify_password(body.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="原密码不正确")
    user_service.validate_password(body.new_password)
    current_user.password_hash = auth.get_password_hash(body.new_password)
    current_user.must_change_password = False
    db.commit()
    return {"message": "密码已更新"}
