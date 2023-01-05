from pathlib import Path

from potyk_ci_back.db import ProjectRepo, create_tables
from potyk_ci_back.models import Project


def setup():
    create_tables()
    try:
        ProjectRepo().save(Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve()))
    except ValueError:
        pass


if __name__ == '__main__':
    setup()
