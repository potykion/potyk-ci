import dataclasses
import datetime as dt
import os
from pathlib import Path
from typing import Optional


@dataclasses.dataclass()
class Project:
    path: Path
    command: str
    name: str
    id: Optional[int] = None

    @classmethod
    def guess(cls, path: Path, **kwargs):
        name = kwargs.get('name', path.name)

        if os.path.exists(path / 'pyproject.toml'):
            command = 'poetry run pytest'
        elif os.path.exists(venv_path := path / 'venv'):
            command = f"{venv_path / 'Scripts' / 'activate.bat'} && pytest"
        else:
            raise ValueError(f'Хз что за проект такой 🤷‍♂️🤷‍♂️🤷‍♂️ ни venv, ни poetry: {path}')

        return cls(path=path, command=command, name=name)


@dataclasses.dataclass()
class QAJob:
    success: bool
    output: str
    project: Project
    created: dt.datetime = dataclasses.field(default_factory=dt.datetime.now)
    id: Optional[int] = None
