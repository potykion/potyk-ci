from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from potyk_ci_back.cases import CreateProject, ScheduleJob, RunCommandsContinuously
from potyk_ci_back.db import ProjectRepo, JobRepo
from potyk_ci_back.dto import ProjectVM, CreateProjectVM, JobVM, CommandVM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/project/list", response_model=List[ProjectVM])
def get_projects():
    projects = ProjectRepo().list()
    return list(map(ProjectVM.from_proj, projects))


@app.get('/project/schedule', response_model=JobVM)
def schedule_project(project_id: int):
    job = ScheduleJob.by_proj_id(project_id)()
    return JobVM.from_model(job)


@app.post('/project/create', response_model=ProjectVM)
def create_project(vm: CreateProjectVM):
    proj = CreateProject(vm)()
    return ProjectVM.from_proj(proj)


@app.get("/qa_job/list_for_project", response_model=List[JobVM])
def list_jobs_for_project(project_id: int):
    qa_jobs = JobRepo().list_for_project(project_id)
    return list(map(JobVM.from_model, qa_jobs))


@app.websocket("/ws-run-step")
async def run_continuously(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        vm = CommandVM.parse_raw(data)
        for line in RunCommandsContinuously.by_proj_id(vm.proj_id, vm.commands)():
            await websocket.send_text(line)
