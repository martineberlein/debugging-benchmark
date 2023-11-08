from pathlib import Path
from typing import List, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from fuzzingbook.Grammars import Grammar

from debugging_benchmark.refactory import BenchmarkProgram, BenchmarkRepository
from debugging_benchmark.tests4py_benchmark.tests4py_api import build_project


class Tests4PyProject:

    def __init__(self, project: Project, grammar: Grammar, initial_inputs: List[str]):
        self.project = project
        self.grammar = grammar
        self.initial_inputs = initial_inputs


@dataclass
class Pysnooper2Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_2
    grammar = project.grammar
    initial_inputs = ["-d1\n-T\n"]

    def __post_init__(self):
        super().__init__(self.project, self.grammar, self.initial_inputs)


@dataclass
class Pysnooper3Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_3
    grammar = project.grammar
    initial_inputs = ["-d1\n-T\n"]

    def __post_init__(self):
        super().__init__(self.project, self.grammar, self.initial_inputs)


if __name__ == "__main__":
    pro = Pysnooper2Tests4PyProject()
    print(pro.initial_inputs)

