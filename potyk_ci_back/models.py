import dataclasses
import datetime as dt
import os
from pathlib import Path
from typing import Optional


@dataclasses.dataclass()
class Project:
    path: Path
    command: str
    id: Optional[int] = None

    @property
    def name(self):
        return self.path.name

    @classmethod
    def guess(cls, path: Path):
        if os.path.exists(path / 'pyproject.toml'):
            return cls(path, 'poetry run pytest')

        venv_path = path / 'venv'
        if os.path.exists(venv_path):
            return cls(path, f"{venv_path / 'Scripts' / 'activate.bat'} && pytest")


@dataclasses.dataclass()
class QAJob:
    success: bool
    output: str
    project: Project
    created: dt.datetime = dataclasses.field(default_factory=dt.datetime.now)
    id: Optional[int] = None
