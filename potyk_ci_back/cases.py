import dataclasses
import os
import subprocess
from itertools import groupby

from potyk_ci_back.db import ProjectRepo, JobRepo, GitRepo, NotifRepo, do_in_transaction
from potyk_ci_back.dto import CreateProjectVM
from potyk_ci_back.models import Project, Job, JobStatus


@dataclasses.dataclass()
class ScheduleJob:
    proj: Project
    job_repo: JobRepo = dataclasses.field(default_factory=JobRepo)

    @classmethod
    def by_proj_id(cls, proj_id):
        return cls(proj=ProjectRepo().get(proj_id))

    def __call__(self, ):
        return self.job_repo.create(Job(project=self.proj))


@dataclasses.dataclass()
class ScheduleJobsForNewCommits:
    project_repo: ProjectRepo = dataclasses.field(default_factory=ProjectRepo)
    qa_job_repo: JobRepo = dataclasses.field(default_factory=JobRepo)
    git_repo: GitRepo = dataclasses.field(default_factory=GitRepo)

    def __call__(self):
        projects = self.project_repo.list()
        for proj in projects:
            if not os.path.exists(proj.path):
                continue

            last_job_run = self.qa_job_repo.last(proj)
            if last_job_run and self.git_repo.check_for_new(proj.path, last_job_run.created):
                ScheduleJob(proj)()


@dataclasses.dataclass()
class RunJob:
    job: Job
    qa_job_repo: JobRepo = dataclasses.field(default_factory=JobRepo)
    notif_repo: NotifRepo = dataclasses.field(default_factory=NotifRepo)

    def __call__(self, ) -> Job:
        res = subprocess.run(
            self.job.project.command,
            shell=True,
            cwd=self.job.project.path,
            text=True,
            capture_output=True,
        )

        job = self.qa_job_repo.update(
            self.job.copy(update={
                'output': res.stdout,
                'status': JobStatus.DONE if not bool(res.returncode) else JobStatus.ERR,
            })
        )

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


@dataclasses.dataclass()
class ProcessPendingJobs:
    job_repo: JobRepo = dataclasses.field(default_factory=JobRepo)

    def __call__(self, *args, **kwargs):
        pending_jobs = self.job_repo.list_pending()
        if pending_jobs:
            print(f'pending_jobs = {len(pending_jobs)}')

        proj_jobs = groupby(pending_jobs, key=lambda job: job.project)
        for proj, jobs in proj_jobs:
            job_to_run, *jobs_to_cancel = jobs
            with do_in_transaction():
                for job in jobs_to_cancel:
                    self.job_repo.cancel(job)

                RunJob(job_to_run)()
