from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from potyk_ci_back.cases import RunQA, CreateProject
from potyk_ci_back.db import ProjectRepo, QAJobRepo
from potyk_ci_back.dto import ProjectVM, CreateProjectVM, QAJobVM

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




@app.get("/project/list", response_model=List[ProjectVM])
def get_projects():
    projects = ProjectRepo().list()
    return list(map(ProjectVM.from_proj, projects))


@app.get('/project/run', response_model=QAJobVM)
def run_project(project_id: int):
    job = RunQA.from_project_id(project_id)()
    return QAJobVM.from_model(job)


@app.post('/project/create', response_model=ProjectVM)
def create_project(vm: CreateProjectVM):
    proj = CreateProject(vm)()
    return ProjectVM.from_proj(proj)


@app.get("/qa_job/list_for_project", response_model=List[QAJobVM])
def list_jobs_for_project(project_id: int):
    qa_jobs = QAJobRepo().list_for_project(project_id)
    return list(map(QAJobVM.from_model, qa_jobs))
