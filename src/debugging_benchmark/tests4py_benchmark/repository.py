from typing import List, Dict
from abc import ABC
import logging

from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.tests4py_benchmark.project import *
from debugging_benchmark.tests4py_benchmark.program import Tests4PyBenchmarkProgram
from debugging_benchmark.tests4py_benchmark.api import (
    build_project,
    construct_oracle,
)


class Tests4PyBenchmarkRepository(BenchmarkRepository, ABC):
    """
    A repository class for handling and constructing benchmark programs specifically
    for Python projects managed by the Tests4Py framework.
    """

    def __init__(
        self,
        projects: List[Tests4PyProject],
        force_checkout=False,
        update_checkout=False,
    ):
        """
        Initializes the repository with a list of Tests4PyProject instances.
        :param List[Tests4PyProject] projects: The projects to be included in the benchmark repository.
        """
        self.projects = projects
        self.force_checkout = force_checkout
        self.update_checkout = update_checkout

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
                build_project(
                    project.project,
                    force=self.force_checkout,
                    update=self.update_checkout,
                )
                program = self._construct_benchmark_program(project)
                constructed_programs.append(program)
            except Exception as e:
                logging.error(f"Failed to build project {project}: {str(e)}")
        return constructed_programs


class PysnooperBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-Pysnooper"
        projects: List[Tests4PyProject] = [
            Pysnooper2Tests4PyProject(),
            Pysnooper3Tests4PyProject(),
        ]
        super().__init__(projects, **kwargs)


class CookieCutterBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-CookieCutter"
        projects: List[Tests4PyProject] = [
            CookieCutter2Tests4PyProject(),
            CookieCutter3Tests4PyProject(),
            # CookieCutter4Tests4PyProject(),
        ]
        super().__init__(projects, **kwargs)


class FastAPIBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-FastAPI"
        projects: List[Tests4PyProject] = [FastAPI1Tests4PyProject()]
        super().__init__(projects, **kwargs)


class MiddleBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-Middle"
        projects: List[Tests4PyProject] = [
            Middle1Tests4PyProject(),
            Middle2Tests4PyProject(),
        ]
        super().__init__(projects, **kwargs)


class CalculatorBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-Calculator"
        projects: List[Tests4PyProject] = [CalculatorTests4PyProject()]
        super().__init__(projects, **kwargs)


class ToyExampleTests4PyBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self, **kwargs):
        self.name = "Tests4Py-ToyExample"
        projects: List[Tests4PyProject] = [
            CalculatorTests4PyProject(),
            ExpressionTests4PyProject(),
            Markup1Tests4PyProject(),
            Markup2Tests4PyProject(),
            Middle1Tests4PyProject(),
            Middle2Tests4PyProject(),
        ]
        super().__init__(projects, **kwargs)
