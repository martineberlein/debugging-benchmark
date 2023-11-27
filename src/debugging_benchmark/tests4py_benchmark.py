from pathlib import Path
from typing import List, Callable

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
    Middle1Tests4PyProject,
    Middle2Tests4PyProject,
    CalculatorTests4PyProject,
    CookieCutter2Tests4PyProject,
    CookieCutter3Tests4PyProject,
    CookieCutter4Tests4PyProject,
    FastAPI1Tests4PyProject,
    ExpressionTests4PyProject,
    Markup1Tests4PyProject,
    Markup2Tests4PyProject,
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
        super().__init__(name, grammar, oracle, initial_inputs)
        self.bug_id = bug_id

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


class Tests4PyBenchmarkRepository(BenchmarkRepository):
    def __init__(self, projects: List[Tests4PyProject]):
        self.projects = projects

    def get_implementation_function_name(self):
        pass

    def get_dir(self) -> Path:
        pass

    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass

    def get_t4p_project(self) -> List[Tests4PyProject]:
        return self.projects

    @staticmethod
    def _construct_benchmark_program(
        t4p_project: Tests4PyProject,
    ) -> Tests4PyBenchmarkProgram:
        oracle = construct_oracle(
            t4p_project.project, harness_function=t4p_project.harness_function
        )
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
        projects: List[Tests4PyProject] = [
            Pysnooper2Tests4PyProject(),
            Pysnooper3Tests4PyProject(),
        ]
        super().__init__(projects)


class CookieCutterBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-CookieCutter"
        projects: List[Tests4PyProject] = [
            CookieCutter2Tests4PyProject(),
            CookieCutter3Tests4PyProject(),
            CookieCutter4Tests4PyProject(),
        ]
        super().__init__(projects)


class FastAPIBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-FastAPI"
        projects: List[Tests4PyProject] = [FastAPI1Tests4PyProject()]
        super().__init__(projects)


class YoutubeDLBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-YoutubeDL"
        projects: List[Tests4PyProject] = [YoutubeDL1Tests4PyProject()]
        super().__init__(projects)


class MiddleBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-Middle"
        projects: List[Tests4PyProject] = [
            Middle1Tests4PyProject(),
            Middle2Tests4PyProject(),
        ]
        super().__init__(projects)


class CalculatorBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-Calculator"
        projects: List[Tests4PyProject] = [CalculatorTests4PyProject()]
        super().__init__(projects)


class ToyExampleTests4PyBenchmarkRepository(Tests4PyBenchmarkRepository):
    def __init__(self):
        self.name = "Tests4Py-ToyExample"
        projects: List[Tests4PyProject] = [
            CalculatorTests4PyProject(),
            ExpressionTests4PyProject(),
            Markup1Tests4PyProject(),
            Markup2Tests4PyProject(),
        ]
        super().__init__(projects)


def main():
    repos: List[Tests4PyBenchmarkRepository] = [
        # YoutubeDLBenchmarkRepository(),
        # CookieCutterBenchmarkRepository(),
        MiddleBenchmarkRepository(),
        # CalculatorBenchmarkRepository()
    ]

    repos: List[Tests4PyBenchmarkRepository] = [
        Tests4PyBenchmarkRepository(
            projects=[
                CalculatorTests4PyProject(),
                ExpressionTests4PyProject(),
                Markup1Tests4PyProject(),
                Markup2Tests4PyProject()
            ]
        )
    ]

    subjects = []
    for repo in repos:
        _subjects = repo.build()
        subjects += _subjects

    for subject in subjects:
        print(subject)
        for inp in subject.initial_inputs:
            print(subject.oracle(inp))


if __name__ == "__main__":
    main()
