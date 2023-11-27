from typing import List, Callable, Union
import shlex
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from fuzzingbook.Grammars import Grammar

from debugging_framework.input import Input
from debugging_framework.types import HARNESS_FUNCTION
from debugging_benchmark.tests4py_helper.tests4py_grammars import (
    grammar_pysnooper,
    grammar_youtube_dl_1,
)
from debugging_benchmark.refactory import BenchmarkProgram, BenchmarkRepository
from debugging_benchmark.tests4py_helper.tests4py_api import build_project


class Tests4PyProject:
    def __init__(
        self,
        project: Project,
        grammar: Grammar,
        initial_inputs: List[str],
        harness_function: HARNESS_FUNCTION,
    ):
        self.project = project
        self.grammar = grammar
        self.initial_inputs = initial_inputs
        self.harness_function: HARNESS_FUNCTION = harness_function


def pysnooper_harness_function(inp: Union[str, Input]) -> List[str]:
    """Parse input into a list of arguments."""
    parts = shlex.split(str(inp))
    return [part for part in parts if part]


def cookiecutter_harness_function(inp: Union[str, Input]) -> List[str]:
    parts = str(inp).split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


def tests_4py_api_harness_function(inp: Union[str, Input]) -> List[str]:
    parts = shlex.split(str(inp))
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


@dataclass
class Pysnooper2Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_2
    grammar = grammar_pysnooper
    initial_inputs = [
        "-o='test.log' -c=int=str ",
        "-d=7 -p='test' -w='e.nest2' -c=bool=str,int=str -O ",
        "-o -d=7 -p='1' -w='e.nest2' -c=bool=str,int=str -T ",
    ]
    harness_function: Callable = pysnooper_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class Pysnooper3Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_3
    grammar = grammar_pysnooper
    initial_inputs = [
        "-o='test7.log' -d=1 -p='test' ",
    ]
    harness_function: Callable = pysnooper_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class CookieCutter2Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_2
    grammar = project.grammar
    initial_inputs = [
        # Passing
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
        # Passing
        '{"full_name":"Martin Eberlein",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1",
    ]
    harness_function: HARNESS_FUNCTION = cookiecutter_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class CookieCutter3Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_3
    grammar = project.grammar
    initial_inputs = [
        # Passing
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
        # Passing
        '{"full_name":"Martin Eberlein",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1",
    ]
    harness_function: HARNESS_FUNCTION = cookiecutter_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class CookieCutter4Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_4
    grammar = project.grammar
    initial_inputs = [
        # Passing
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
        # Passing
        '{"full_name":"Martin Eberlein",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1",
    ]
    harness_function: HARNESS_FUNCTION = cookiecutter_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class FastAPI1Tests4PyProject(Tests4PyProject):
    project: Project = api.fastapi_1
    grammar = project.grammar
    initial_inputs = [
        "-o\"{'foo':'test'}\" -d",
        "-o\"{'foo':'test'}\"",
    ]
    harness_function: HARNESS_FUNCTION = tests_4py_api_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


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


@dataclass
class Middle1Tests4PyProject(Tests4PyProject):
    project: Project = api.middle_1
    grammar = project.grammar
    initial_inputs = ["4 2 5", "2 4 5"]
    harness_function: HARNESS_FUNCTION = tests_4py_api_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class Middle2Tests4PyProject(Tests4PyProject):
    project: Project = api.middle_2
    grammar = project.grammar
    initial_inputs = ["4 2 5", "2 4 5"]
    harness_function: HARNESS_FUNCTION = tests_4py_api_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


@dataclass
class CalculatorTests4PyProject(Tests4PyProject):
    project: Project = api.calculator_1
    grammar = project.grammar
    initial_inputs = [
        "cos(-900)",
        "sqrt(-100)",
    ]
    harness_function: HARNESS_FUNCTION = tests_4py_api_harness_function

    def __post_init__(self):
        super().__init__(
            self.project, self.grammar, self.initial_inputs, self.harness_function
        )


if __name__ == "__main__":
    pro = CookieCutter2Tests4PyProject()
    print(pro.grammar)
