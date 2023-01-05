import datetime as dt
from pathlib import Path

import pytest

from potyk_ci_back.db import ProjectRepo, JobRepo, NotifRepo
from potyk_ci_back.models import Project, Job, JobStatus


@pytest.fixture()
def project(project_path):
    return ProjectRepo().save(Project.guess(project_path))


@pytest.fixture()
def qa_job(project):
    return JobRepo().create(Job(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 1)))


def test_ProjectRepo_list(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    proj = (repo := ProjectRepo()).save(proj)

    projects = repo.list()

    assert projects == [proj]


def test_QAJobRepo_last(mock_db, project):
    job_1 = (repo := JobRepo()).create(Job(project=project, created=dt.datetime(2022, 12, 1)))
    job_2 = repo.create(Job(project=project, created=dt.datetime(2022, 12, 2)))

    last = repo.last(project)

    assert last == job_2


def test_JobRepo_Update(project):
    job = (repo := JobRepo()).create(Job(project=project, created=dt.datetime(2022, 12, 1)))

    job = job.copy(update={'output': 'ok', 'status': JobStatus.DONE})
    repo.update(job)

    assert repo.get_by_id(job.id) == job


def test_QAJobRepo_last_returns_none(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    proj = ProjectRepo().save(proj)

    last = JobRepo().last(proj)

    assert last is None


@pytest.mark.skip()
def test_NotifRepo_send(qa_job):
    NotifRepo().send(qa_job)
