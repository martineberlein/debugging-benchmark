from pathlib import Path
from typing import List, Callable
from abc import ABC, abstractmethod

from tests4py import api
from tests4py.projects import Project

from fuzzingbook.Grammars import Grammar

from debugging_framework.benchmark import BenchmarkProgram
from debugging_benchmark.refactory import BenchmarkRepository
from debugging_benchmark.tests4py_helper.tests4py_api import (
    build_project,
    construct_oracle,
)
from debugging_benchmark.tests4py_helper.tests4py_projects import (
    Tests4PyProject,
    Pysnooper2Tests4PyProject,
    Pysnooper3Tests4PyProject,
    YoutubeDL1Tests4PyProject,
)


class Tests4PyBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        initial_inputs: List[str],
        oracle: Callable,
    ):
        super().__init__(name, grammar, oracle)
        self.name = name
        self.bug_id = bug_id
        self.grammar = grammar
        self.initial_inputs = initial_inputs
        self.oracle = oracle

    def __repr__(self):
        return f"Program({self.name}_{self.bug_id})"

    def get_name(self) -> str:
        return self.__repr__()

    def get_grammar(self):
        return self.grammar

    def get_initial_inputs(self):
        return self.initial_inputs

    def get_oracle(self):
        return self.oracle


class Tests4PyBenchmarkRepository(BenchmarkRepository, ABC):
    def get_implementation_function_name(self):
        pass

    def get_dir(self) -> Path:
        pass

    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass

    @abstractmethod
    def get_grammar_for_project(self, project: Tests4PyProject):
        raise NotImplementedError

    @abstractmethod
    def get_t4p_project(self) -> List[Tests4PyProject]:
        raise NotImplementedError()

    @staticmethod
    def _construct_benchmark_program(
        t4p_project: Tests4PyProject,
    ) -> Tests4PyBenchmarkProgram:
        oracle = construct_oracle(t4p_project.project)
        return Tests4PyBenchmarkProgram(
            name=t4p_project.project.project_name,
            bug_id=t4p_project.project.bug_id,
            grammar=t4p_project.grammar,
            initial_inputs=t4p_project.initial_inputs,
            oracle=oracle,
        )

    def build(self) -> List[Tests4PyBenchmarkProgram]:
        constructed_programs: List[Tests4PyBenchmarkProgram] = []

        for t4p_project in self.get_t4p_project():
            build_project(t4p_project.project)
            constructed_program = self._construct_benchmark_program(t4p_project)
            constructed_programs.append(constructed_program)

        return constructed_programs


class PysnooperBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-Pysnooper"
        self.projects: List[Tests4PyProject] = [
            Pysnooper2Tests4PyProject(),
            Pysnooper3Tests4PyProject(),
        ]

    def get_grammar_for_project(self, project: Tests4PyProject):
        return project.grammar

    def get_t4p_project(self) -> List[Tests4PyProject]:
        return self.projects


class YoutubeDLBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-YoutubeDL"
        self.projects: List[Tests4PyProject] = [
            YoutubeDL1Tests4PyProject(),
        ]

    def get_grammar_for_project(self, project: Tests4PyProject):
        return project.grammar

    def get_t4p_project(self) -> List[Tests4PyProject]:
        return self.projects


def main():
    project: Project = api.pysnooper_2
    print(project.project_name, project.bug_id)
    print(project.grammar)

    repo = PysnooperBenchmarkRepository()
    print(repo.name)
    subjects = repo.build()
    for subject in subjects:
        print(subject)
        for inp in subject.initial_inputs:
            print(subject.oracle(inp))


if __name__ == "__main__":
    main()
