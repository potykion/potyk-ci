import datetime as dt
from pathlib import Path

from pydantic import BaseModel


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
