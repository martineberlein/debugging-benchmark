from typing import List, Dict
from abc import ABC
import logging

from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.tests4py.project import Tests4PyProject
from debugging_benchmark.tests4py.program import Tests4PyBenchmarkProgram
from debugging_benchmark.tests4py.tests4py_api import (
    build_project,
    construct_oracle,
)


class Tests4PyBenchmarkRepository(BenchmarkRepository, ABC):
    """
    A repository class for handling and constructing benchmark programs specifically
    for Python projects managed by the Tests4Py framework.
    """

    def __init__(self, projects: List[Tests4PyProject]):
        """
        Initializes the repository with a list of Tests4PyProject instances.
        :param List[Tests4PyProject] projects: The projects to be included in the benchmark repository.
        """
        self.projects = projects

    @staticmethod
    def _construct_benchmark_program(
        t4p_project: Tests4PyProject,
    ) -> Tests4PyBenchmarkProgram:
        """
        Constructs a Tests4PyBenchmarkProgram from a Tests4PyProject instance. This method
        encapsulates the process of oracle construction and program setup based on the project details.
        :param Tests4PyProject t4p_project: The project from which to construct the benchmark program.
        :return Tests4PyBenchmarkProgram: The constructed benchmark program.
        """
        oracle = construct_oracle(
            t4p_project.project, harness_function=t4p_project.harness_function
        )
        return Tests4PyBenchmarkProgram(
            name=t4p_project.project.project_name,
            bug_id=t4p_project.project.bug_id,
            grammar=t4p_project.grammar,
            failing_inputs=t4p_project.failing_inputs,
            passing_inputs=t4p_project.passing_inputs,
            oracle=oracle,
        )

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[Tests4PyBenchmarkProgram]:
        """
        Builds and returns a list of Tests4PyBenchmarkProgram instances for all projects
        in the repository. Each project is built using the Tests4Py API and then transformed
        into a benchmark program.
        :param Dict[Exception, OracleResult] err_def: (Optional) A dictionary mapping exceptions
        to OracleResults, used to define specific error behaviors for the benchmarks.
        :param OracleResult default_oracle: (Optional) A default oracle result to use if no specific
        behavior is defined for an exception.
        :return List[Tests4PyBenchmarkProgram]: A list of constructed benchmark programs.
        """

        constructed_programs = []
        for project in self.projects:
            try:
                build_project(project.project)
                program = self._construct_benchmark_program(project)
                constructed_programs.append(program)
            except Exception as e:
                logging.error(f"Failed to build project {project.__name__}: {str(e)}")
        return constructed_programs
