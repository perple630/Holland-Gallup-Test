import os

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, migrate_schema

from app.routers import auth, assessments, reports, teacher, admin



Base.metadata.create_all(bind=engine)

migrate_schema()



_default_origins = "http://localhost:5173,http://localhost:5175,http://127.0.0.1:5173,http://127.0.0.1:5175"

_cors_origins = [

    o.strip()

    for o in os.environ.get("CORS_ORIGINS", _default_origins).split(",")

    if o.strip()

]



app = FastAPI(

    title="RIASEC × CliftonStrengths 在线测评平台",

    description="双维度职业测评工具",

    version="1.1.0"

)



app.add_middleware(

    CORSMiddleware,

    allow_origins=_cors_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



app.include_router(auth.router)

app.include_router(assessments.router)

app.include_router(reports.router)

app.include_router(teacher.router)

app.include_router(admin.router)





@app.get("/")

def root():

    return {"message": "Assessment Platform API", "version": "1.1.0"}


