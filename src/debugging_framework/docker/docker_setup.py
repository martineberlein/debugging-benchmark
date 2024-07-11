import sys

from debugging_benchmark.tests4py_benchmark.repository import *

if __name__ == "__main__":
    project_name = sys.argv[1] if len(sys.argv) > 1 else "No project provided"
    bug_id = int(sys.argv[2]) if len(sys.argv) > 2 else "No bug id provided"

    match project_name:
        case "pysnooper":
            projects = PysnooperBenchmarkRepository().build()
        case "cookiecutter":
            projects = CookieCutterBenchmarkRepository().build()
        case "fastapi":
            # projects = FastAPIBenchmarkRepository().build()
            pass
        case _:
            raise Exception(f"Unknown project name: {project_name}")

    project = projects[bug_id]
    project.dump(".")
