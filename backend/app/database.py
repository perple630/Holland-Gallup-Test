from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'assessment.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

_USER_COLUMN_MIGRATIONS = [
    ("email", "VARCHAR"),
    ("grade", "VARCHAR"),
    ("class_name", "VARCHAR"),
    ("school", "VARCHAR"),
    ("phone", "VARCHAR"),
    ("career_note", "TEXT"),
    ("profile_complete", "INTEGER DEFAULT 0"),
    ("must_change_password", "INTEGER DEFAULT 0"),
    ("is_active", "INTEGER DEFAULT 1"),
    ("created_by", "VARCHAR"),
    ("updated_at", "DATETIME"),
]


def migrate_schema():
    """为已有 SQLite 数据库补充 users 表新列（幂等）。"""
    with engine.connect() as conn:
        rows = conn.execute(text("PRAGMA table_info(users)")).fetchall()
        existing = {row[1] for row in rows}
        if not existing:
            return
        for col, col_type in _USER_COLUMN_MIGRATIONS:
            if col not in existing:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {col_type}"))
        conn.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
