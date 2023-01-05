import dataclasses
import datetime as dt
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List

from git import Repo
from notifypy import Notify
from peewee import *

from potyk_ci_back.config import BASE_DIR
from potyk_ci_back.models import Job, Project, JobStatus

_db = SqliteDatabase(BASE_DIR / f'{os.environ["COMPUTERNAME"]}.db')


@contextmanager
def do_in_transaction():
    with _db.atomic():
        yield


class ProjectRow(Model):
    path = CharField()
    command = CharField()
    name = CharField()

    class Meta:
        database = _db


class ProjectRepo:
    def list(self) -> List[Project]:
        return [
            self.project_from_row(row)
            for row in ProjectRow.select()
        ]

    @classmethod
    def project_from_row(cls, row):
        return Project(
            path=Path(row.path).resolve(),
            command=row.command,
            id=row.id,
            name=row.name,
        )

    def save(self, project: Project):
        return dataclasses.replace(
            project,
            id=ProjectRow.create(
                path=str(project.path),
                command=project.command,
                name=project.name,
            ).id
        )

    def get(self, project_id):
        return self.project_from_row(ProjectRow.get_by_id(project_id))


class JobRow(Model):
    project = ForeignKeyField(ProjectRow)
    created = DateTimeField()
    output = TextField()
    status = CharField()

    class Meta:
        database = _db


class JobRepo:
    def last(self, proj: Project) -> Optional[Job]:
        try:
            row = (
                JobRow.select()
                .where(JobRow.project == proj.id)
                .order_by(JobRow.created.desc())
                .get()
            )
        except DoesNotExist:
            return None
        else:
            return self.job_from_row(row)

    def job_from_row(self, row: JobRow):
        return Job(
            status=row.status,
            output=row.output,
            project=ProjectRepo.project_from_row(row.project),
            created=row.created,
            id=row.id,
        )

    def job_to_row(self, job, with_id=True):
        row_d = dict(
            project=job.project.id,
            created=job.created,
            status=job.status,
            output=job.output,
        )
        if with_id:
            row_d['id'] = job.id
        return row_d

    def get_by_id(self, job_id):
        return self.job_from_row(JobRow.get_by_id(job_id))

    def update(self, job: Job):
        JobRow(**self.job_to_row(job)).save()
        return job

    def create(self, job: Job):
        row = JobRow.create(**self.job_to_row(job, with_id=False))
        return job.copy(update=dict(id=row.id))

    def list_for_project(self, project_id: int) -> List[Job]:
        rows = (
            JobRow.select()
            .where(JobRow.project == project_id)
            .order_by(JobRow.created.desc())
        )
        return list(map(self.job_from_row, rows))

    def list_pending(self):
        rows = (
            JobRow.select()
            .where(JobRow.status == JobStatus.PENDING)
            .order_by(JobRow.project, JobRow.created.desc())
        )
        return list(map(self.job_from_row, rows))

    def cancel(self, job):
        return self.create(job.copy(status=JobStatus.CANCELLED))


class GitRepo:
    def check_for_new(self, repo_path: Path, from_dt: dt.datetime) -> bool:
        from_dt = from_dt.astimezone()
        commits = Repo(repo_path).iter_commits()
        commits = (c for c in commits if c.committed_datetime > from_dt)
        return any(commits)


TABLES = [
    ProjectRow, JobRow,
]


def create_tables():
    _db.create_tables(TABLES)


class NotifRepo:
    def send(self, qa_job: Job):
        notification = Notify()
        notification.application_name = qa_job.project.name
        notification.title = qa_job.project.command
        notification.message = qa_job.output
        icon_dir = Path(__file__).resolve().parent
        notification.icon = icon_dir / ('ok.png' if qa_job.success else 'err.png')
        notification.send()
