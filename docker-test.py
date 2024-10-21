from typing import List

from debugging_framework.docker.manager import DockerManagerNew

from tests4py.projects import Project
from tests4py import api

if __name__ == "__main__":

    #project: Project = api.get_projects("calculator", 1).pop()
    project: Project = api.get_projects("fastapi", 1).pop()
    assert project, "Project not found!"
    print(project, project.project_name, project.bug_id, project.python_version)

    manager = DockerManagerNew(project)

    try:
        print("Starting")
        manager.build()
        print("Built")
        manager.build_container(7)


        # inputs = ["sqrt(-1)", "cos(900)"]
        # from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer
        # from debugging_benchmark.calculator.calculator import calculator_grammar
        # fuzzer = GrammarFuzzer(calculator_grammar)
        # for _ in range(100):
        #     inputs.append(fuzzer.fuzz())
        from debugging_benchmark.tests4py_benchmark.project import Fastapi1Tests4PyProject

        pro = Fastapi1Tests4PyProject()
        inputs = pro.failing_inputs + pro.passing_inputs

        output = manager.run_inputs(inputs)
        for inp in inputs:
            print(f"Input: {inp}, Output: {output[hash(inp)]}")
        #print(output)
        # manager.run()
        # manager.run()
        # manager.run()
        manager.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error: {e}")
        manager.cleanup()
        exit(1)
