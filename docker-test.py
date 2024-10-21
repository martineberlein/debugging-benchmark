from debugging_framework.docker.manager import DockerManager

if __name__ == "__main__":

    from debugging_benchmark.tests4py_benchmark.project import (
        Fastapi3Tests4PyProject as Subproject,
    )

    t4p_project = Subproject()
    inputs = t4p_project.failing_inputs + t4p_project.passing_inputs

    with DockerManager(t4p_project.project) as docker_manager:
        docker_manager.build()
        docker_manager.build_container(number_of_containers=5)

        # Run inputs and get OracleResult outputs
        outputs = docker_manager.run_inputs(inputs)

        # Print the OracleResults
        for input_str, oracle_result in outputs.items():
            print(f"Input: '{input_str}' : OracleResult: {oracle_result}")
