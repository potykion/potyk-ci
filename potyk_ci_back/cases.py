import dataclasses
import os
import subprocess

from potyk_ci_back.db import ProjectRepo, QAJobRepo, GitRepo, NotifRepo
from potyk_ci_back.models import Project, QAJob


@dataclasses.dataclass()
class CILoop:
    project_repo: ProjectRepo = dataclasses.field(default_factory=ProjectRepo)
    qa_job_repo: QAJobRepo = dataclasses.field(default_factory=QAJobRepo)
    git_repo: GitRepo = dataclasses.field(default_factory=GitRepo)
    notif_repo: NotifRepo = dataclasses.field(default_factory=NotifRepo)

    def __call__(self):
        projects = self.project_repo.list()
        for proj in projects:
            if not os.path.exists(proj.path):
                continue

            last_job_run = self.qa_job_repo.last(proj)
            if not last_job_run or (self.git_repo.check_for_new(proj.path, last_job_run.created)):
                job: QAJob = RunQA(proj)()
                job = self.qa_job_repo.save(job)
                self.notif_repo.send(job)


@dataclasses.dataclass()
class RunQA:
    proj: Project

    def __call__(self, ) -> QAJob:
        res = subprocess.run(
            self.proj.command,
            shell=True,
            cwd=self.proj.path,
            text=True,
            capture_output=True,
        )
        success = not bool(res.returncode)
        return QAJob(success, res.stdout, project=self.proj)