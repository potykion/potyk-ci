import datetime as dt
from pathlib import Path

from pydantic import BaseModel

from potyk_ci_back.models import JobStatus


class CreateProjectVM(BaseModel):
    path: Path
    name: str


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


class JobVM(BaseModel):
    status: JobStatus
    output: str
    created: dt.datetime
    id: int

    @classmethod
    def from_model(cls, job):
        return cls(
            status=job.status,
            output=job.output,
            created=job.created,
            id=job.id,
        )


class Command(BaseModel):
    command: str
    path: Path
