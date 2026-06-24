from datetime import datetime, timedelta
from typing import Optional, Iterable
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas
from app.database import get_db
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已停用")
    return user


def require_roles(*roles: models.UserRole):
    allowed = set(roles)

    def checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in allowed:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user

    return checker


def require_teacher(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in (models.UserRole.teacher, models.UserRole.admin):
        raise HTTPException(status_code=403, detail="需要教师或管理员权限")
    return current_user


def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


def get_or_create_assessment(db: Session, user_id: str):
    assessment = db.query(models.AssessmentStatus).filter(
        models.AssessmentStatus.user_id == user_id
    ).first()
    if not assessment:
        assessment = models.AssessmentStatus(user_id=user_id)
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
    return assessment


def build_token_response(user: models.User) -> dict:
    access_token = create_access_token({"sub": user.id, "role": user.role.value})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role.value,
        "user_id": user.id,
        "username": user.username,
        "display_name": user.display_name,
        "profile_complete": bool(user.profile_complete),
        "must_change_password": bool(user.must_change_password),
    }
