import dataclasses
import os
import subprocess

from potyk_ci_back.db import ProjectRepo, QAJobRepo, GitRepo, NotifRepo
from potyk_ci_back.dto import CreateProjectVM
from potyk_ci_back.models import Project, QAJob


@dataclasses.dataclass()
class CILoop:
    project_repo: ProjectRepo = dataclasses.field(default_factory=ProjectRepo)
    qa_job_repo: QAJobRepo = dataclasses.field(default_factory=QAJobRepo)
    git_repo: GitRepo = dataclasses.field(default_factory=GitRepo)

    def __call__(self):
        projects = self.project_repo.list()
        for proj in projects:
            if not os.path.exists(proj.path):
                continue

            last_job_run = self.qa_job_repo.last(proj)
            if not last_job_run or (self.git_repo.check_for_new(proj.path, last_job_run.created)):
                RunQA(proj)()


@dataclasses.dataclass()
class RunQA:
    proj: Project
    qa_job_repo: QAJobRepo = dataclasses.field(default_factory=QAJobRepo)
    notif_repo: NotifRepo = dataclasses.field(default_factory=NotifRepo)

    @classmethod
    def from_project_id(cls, proj_id):
        return cls(ProjectRepo().get(proj_id))

    def __call__(self, ) -> QAJob:
        res = subprocess.run(
            self.proj.command,
            shell=True,
            cwd=self.proj.path,
            text=True,
            capture_output=True,
        )
        success = not bool(res.returncode)
        job = QAJob(success, res.stdout, project=self.proj)
        job = self.qa_job_repo.save(job)
        self.notif_repo.send(job)
        return job


@dataclasses.dataclass()
class CreateProject:
    vm: CreateProjectVM
    project_repo: ProjectRepo = dataclasses.field(default_factory=ProjectRepo)

    def __call__(self) -> Project:
        return self.project_repo.save(
            Project.guess(self.vm.path, name=self.vm.name)
        )
