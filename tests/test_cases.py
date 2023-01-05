from potyk_ci_back.cases import CreateProject
from potyk_ci_back.dto import CreateProjectVM


def test_create_project(project_path):
    name = 'name'

    proj = CreateProject(CreateProjectVM(path=project_path, name=name))()

    assert proj.id
    assert proj.path == project_path
    assert proj.name == name
