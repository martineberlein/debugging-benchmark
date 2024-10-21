from typing import List

from debugging_framework.docker.manager import DockerManagerNew

from tests4py.projects import Project
from tests4py import api

if __name__ == "__main__":

    from debugging_benchmark.tests4py_benchmark.project import (
        Fastapi3Tests4PyProject as Subproject,
    )

    # from debugging_benchmark.tests4py_benchmark.project import Calculator1Tests4PyProject as Subproject

    pro = Subproject()
    inputs = pro.failing_inputs + pro.passing_inputs
    project = pro.project

    with DockerManagerNew(project) as docker_manager:
        docker_manager.build()
        docker_manager.build_container(number_of_containers=5)
        # Run inputs and get OracleResult outputs
        outputs = docker_manager.run_inputs(inputs)

        # Print the OracleResults
        for input_str, oracle_result in outputs.items():
            print(f"Input: '{input_str}' : OracleResult: {oracle_result}")
