from pathlib import Path
from typing import List, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from fuzzingbook.Grammars import Grammar

from debugging_benchmark.tests4py_helper.tests4py_grammars import grammar_pysnooper, grammar_youtube_dl_1
from debugging_benchmark.refactory import BenchmarkProgram, BenchmarkRepository
from debugging_benchmark.tests4py_helper.tests4py_api import build_project


class Tests4PyProject:

    def __init__(self, project: Project, grammar: Grammar, initial_inputs: List[str]):
        self.project = project
        self.grammar = grammar
        self.initial_inputs = initial_inputs


@dataclass
class Pysnooper2Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_2
    grammar = grammar_pysnooper
    initial_inputs = ["-o='test.log' -c=int=str "]

    def __post_init__(self):
        super().__init__(self.project, self.grammar, self.initial_inputs)


@dataclass
class Pysnooper3Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_3
    grammar = grammar_pysnooper
    initial_inputs = ["-o='test7.log' -d=1 -p='test' "]

    def __post_init__(self):
        super().__init__(self.project, self.grammar, self.initial_inputs)


@dataclass
class YoutubeDL1Tests4PyProject(Tests4PyProject):
    project: Project = api.youtubedl_1
    grammar = grammar_youtube_dl_1
    initial_inputs = [
        "-q '!like_count' -d {'dislike_count': 85}",
        "-q '!is_live' -d {'is_live': False}",
        "-q 'test >? 0' -d {}",
    ]

    def __post_init__(self):
        super().__init__(self.project, self.grammar, self.initial_inputs)


if __name__ == "__main__":
    pro = YoutubeDL1Tests4PyProject()
    print(pro.initial_inputs)

