import datetime as dt
from pathlib import Path
from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

from potyk_ci_back.cases import RunQA
from potyk_ci_back.db import ProjectRepo, QAJobRepo
from potyk_ci_back.models import Project, QAJob

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectVM(BaseModel):
    path: Path
    command: str
    id: int
    name: str

    @classmethod
    def from_proj(cls, proj):
        return cls(
            id=proj.id,
            name=proj.name,
            path=proj.path,
            command=proj.command,
        )


class QAJobVM(BaseModel):
    success: bool
    output: str
    created: dt.datetime
    id: int

    @classmethod
    def from_model(cls, qa_job):
        return cls(
            success=qa_job.success,
            output=qa_job.output,
            created=qa_job.created,
            id=qa_job.id,
        )


@app.get("/project/list", response_model=List[ProjectVM])
def get_projects():
    projects = ProjectRepo().list()
    return list(map(ProjectVM.from_proj, projects))


@app.get('/project/run', response_model=QAJobVM)
def run_project(project_id: int):
    proj = ProjectRepo().get(project_id)
    job = RunQA(proj)()
    return QAJobVM.from_model(job)


@app.get("/qa_job/list_for_project", response_model=List[QAJobVM])
def list_jobs_for_project(project_id: int):
    qa_jobs = QAJobRepo().list_for_project(project_id)
    return list(map(QAJobVM.from_model, qa_jobs))
