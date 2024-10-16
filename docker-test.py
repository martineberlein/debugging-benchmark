from typing import List

from debugging_framework.docker.manager import DockerManagerNew

from tests4py.projects import Project
from tests4py import api

if __name__ == "__main__":

    project: Project = api.get_projects("fastapi", 1).pop()
    assert project, "Project not found!"
    print(project, project.project_name, project.bug_id, project.python_version)

    manager = DockerManagerNew(project)

    try:
        print("Starting")
        manager.build()
        print("Built")
        manager.build_container(7)
        manager.run()
        manager.run()
        manager.run()
        manager.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error: {e}")
        manager.cleanup()
        exit(1)
