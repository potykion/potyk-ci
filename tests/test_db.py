import datetime as dt
from pathlib import Path

import pytest

from potyk_ci_back.db import ProjectRepo, QAJobRepo, NotifRepo
from potyk_ci_back.models import Project, QAJob


@pytest.fixture()
def project(project_path):
    return ProjectRepo().save(Project.guess(project_path))


@pytest.fixture()
def qa_job(project):
    return QAJobRepo().save(QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 1)))


def test_ProjectRepo_list(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    proj = (repo := ProjectRepo()).save(proj)

    projects = repo.list()

    assert projects == [proj]


def test_QAJobRepo_last(mock_db, project):
    (repo := QAJobRepo()).save(QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 1)))
    qa_job = repo.save(QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 2)))

    last = repo.last(project)

    assert last == qa_job


def test_QAJobRepo_last_returns_none(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    proj = ProjectRepo().save(proj)

    last = QAJobRepo().last(proj)

    assert last is None


# def test_NotifRepo_send(qa_job):
#     NotifRepo().send(qa_job)
