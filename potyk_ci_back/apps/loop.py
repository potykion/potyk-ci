from pathlib import Path
from time import sleep

from potyk_ci_back.cases import CILoop
from potyk_ci_back.db import ProjectRepo, create_tables
from potyk_ci_back.models import Project


def setup():
    create_tables()
    proj = Project.guess(Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve())
    (repo := ProjectRepo()).save(proj)


# setup()
def main():
    while True:
        CILoop()()
        sleep(1)


if __name__ == '__main__':
    main()
