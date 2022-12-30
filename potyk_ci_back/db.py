import dataclasses
import datetime as dt
from pathlib import Path
from typing import Optional, List

from git import Repo
from notifypy import Notify
from peewee import *

from potyk_ci_back.models import QAJob, Project

db = SqliteDatabase('qa.db')


class ProjectTable(Model):
    path = CharField()
    command = CharField()

    class Meta:
        database = db


class ProjectRepo:
    def list(self) -> List[Project]:
        return [
            self.project_from_row(row)
            for row in ProjectTable.select()
        ]

    @classmethod
    def project_from_row(cls, row):
        return Project(path=Path(row.path).resolve(), command=row.command, id=row.id)

    def save(self, project: Project):
        return dataclasses.replace(
            project,
            id=ProjectTable.create(
                path=str(project.path),
                command=project.command,
            ).id
        )

    def get(self, project_id):
        return self.project_from_row(ProjectTable.get_by_id(project_id))


class QAJobTable(Model):
    project = ForeignKeyField(ProjectTable)
    created = DateTimeField()
    success = BooleanField()
    output = TextField()

    class Meta:
        database = db


class QAJobRepo:
    def last(self, proj: Project) -> Optional[QAJob]:
        try:
            row = (
                QAJobTable.select()
                .where(QAJobTable.project == proj.id)
                .order_by(QAJobTable.created.desc())
                .get()
            )
        except DoesNotExist:
            return None
        else:
            return self.qa_job_from_row(row)

    def qa_job_from_row(self, row):
        return QAJob(
            success=row.success,
            output=row.output,
            project=ProjectRepo.project_from_row(row.project),
            created=row.created,
            id=row.id,
        )

    def save(self, job: QAJob):
        return dataclasses.replace(
            job,
            id=QAJobTable.create(
                project=job.project.id,
                created=job.created,
                success=job.success,
                output=job.output,
            ).id,
        )

    def list_for_project(self, project_id: int) -> List[QAJob]:
        rows = (
            QAJobTable.select()
            .where(QAJobTable.project == project_id)
            .order_by(QAJobTable.created.desc())
        )
        return list(map(self.qa_job_from_row, rows))


class GitRepo:
    def check_for_new(self, repo_path: Path, from_dt: dt.datetime) -> bool:
        from_dt = from_dt.astimezone()
        commits = Repo(repo_path).iter_commits()
        commits = (c for c in commits if c.committed_datetime > from_dt)
        return any(commits)


TABLES = [
    ProjectTable, QAJobTable,
]


def create_tables():
    db.create_tables(TABLES)


class NotifRepo:
    def send(self, qa_job: QAJob):
        notification = Notify()
        notification.application_name = qa_job.project.name
        notification.title = qa_job.project.command
        notification.message = qa_job.output
        icon_dir = Path(__file__).resolve().parent
        notification.icon = icon_dir / ('ok.png' if qa_job.success else 'err.png')
        notification.send()
