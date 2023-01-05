import dataclasses
import datetime as dt
import enum
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


@dataclasses.dataclass(frozen=True)
class Project:
    path: Path
    command: str
    name: str
    id: Optional[int] = None

    @classmethod
    def guess(cls, path: Path, **kwargs):
        if not os.path.exists(path):
            raise ValueError('Нет такого проекта')

        name = kwargs.get('name', path.name)

        if os.path.exists(path / 'pyproject.toml'):
            command = 'poetry run pytest'
        elif os.path.exists(venv_path := path / 'venv'):
            command = f"{venv_path / 'Scripts' / 'activate.bat'} && pytest"
        else:
            raise ValueError(f'Хз что за проект такой 🤷‍♂️🤷‍♂️🤷‍♂️ ни venv, ни poetry: {path}')

        return cls(path=path, command=command, name=name)


class JobStatus(str, enum.Enum):
    DONE = 'DONE'
    ERR = 'ERR'
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'

    @classmethod
    def from_bool(cls, bool_: bool):
        return cls.DONE if bool_ else cls.ERR


class Job(BaseModel):
    output: str = ''
    project: Project
    status: JobStatus = JobStatus.PENDING
    created: dt.datetime = Field(default_factory=dt.datetime.now)
    id: Optional[int] = None

    @property
    def success(self):
        return self.status == JobStatus.DONE
