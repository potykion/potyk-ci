from time import sleep

from potyk_ci_back.cases import ProcessPendingJobs, ScheduleJobsForNewCommits


def main():
    while True:
        ScheduleJobsForNewCommits()()
        ProcessPendingJobs()()
        sleep(1)


if __name__ == '__main__':
    main()
