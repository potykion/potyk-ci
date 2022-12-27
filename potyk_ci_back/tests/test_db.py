from pathlib import Path
import datetime as dt

import pytest
from peewee import SqliteDatabase

from potyk_ci_back.db import TABLES, ProjectRepo, QAJobRepo, NotifRepo
from potyk_ci_back.models import Project, QAJob

test_db = SqliteDatabase(':memory:')


@pytest.fixture()
def mock_db():
    test_db.bind(TABLES, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(TABLES)
    yield
    test_db.drop_tables(TABLES)
    test_db.close()


@pytest.fixture()
def project(mock_db):
    return ProjectRepo().save(Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve()))


@pytest.fixture()
def qa_job(project):
    return QAJobRepo().save(QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 1)))


def test_ProjectRepo_list(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    (repo := ProjectRepo()).save(proj)

    projects = repo.list()

    assert projects == [proj]


def test_QAJobRepo_last(mock_db, project):
    (repo := QAJobRepo()).save(QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 1)))
    repo.save(qa_job := QAJob(success=True, output='ok', project=project, created=dt.datetime(2022, 12, 2)))

    last = repo.last(project)

    assert last == qa_job


def test_QAJobRepo_last_returns_none(mock_db):
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    proj = ProjectRepo().save(proj)

    last = QAJobRepo().last(proj)

    assert last is None


def test_NotifRepo_send(qa_job):
    NotifRepo().send(qa_job)
