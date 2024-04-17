from typing import List, Callable, Union
import shlex
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from debugging_framework.types import Grammar

from debugging_framework.input.input import Input
from debugging_framework.types import HarnessFunctionType
from debugging_benchmark.tests4py.grammars import (
    grammar_pysnooper,
    grammar_youtube_dl_1,
)


def default_tests4py_api_harness_function(inp: Union[str, Input]) -> List[str]:
    parts = shlex.split(str(inp))
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


class Tests4PyProject:
    def __init__(
        self,
        project: Project,
        grammar: Grammar,
        failing_inputs: List[str],
        passing_inputs: List[str],
        harness_function: HarnessFunctionType = default_tests4py_api_harness_function,
    ):
        self.project = project
        self.grammar = grammar
        self.failing_inputs = failing_inputs
        self.passing_inputs = passing_inputs
        self.harness_function: HarnessFunctionType = harness_function


def pysnooper_harness_function(inp: Union[str, Input]) -> List[str]:
    """Parse input into a list of arguments."""
    parts = shlex.split(str(inp))
    return [part for part in parts if part]


def cookiecutter_harness_function(inp: Union[str, Input]) -> List[str]:
    parts = str(inp).split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


def markup_harness_function(inp: Union[str, Input]) -> List[str]:
    return [str(inp)]


@dataclass
class Pysnooper2Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_2
    grammar = grammar_pysnooper
    failing_inputs = [
        "-o='test.log' -c=int=str ",
        "-d=7 -p='test' -w='e.nest2' -c=bool=str,int=str -O ",
        "-o -d=7 -p='1' -w='e.nest2' -c=bool=str,int=str -T ",
    ]
    passing_inputs = ["-o='test7.log' -d=1 -p='test' "]
    harness_function: Callable = pysnooper_harness_function


@dataclass
class Pysnooper3Tests4PyProject(Tests4PyProject):
    project: Project = api.pysnooper_3
    grammar = grammar_pysnooper
    failing_inputs = [
        "-o='test7.log' -d=1 -p='test' ",
    ]
    passing_inputs = ["-d=7 -p='1'"]
    harness_function: Callable = pysnooper_harness_function


@dataclass
class CookieCutter2Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_2
    grammar = project.grammar
    failing_inputs = [
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
    ]
    passing_inputs = [
        '{"full_name":"Martin Eberlein",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1",
    ]
    harness_function: HarnessFunctionType = cookiecutter_harness_function


@dataclass
class CookieCutter3Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_3
    grammar = project.grammar
    failing_inputs = [
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
    ]
    passing_inputs = [
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
    harness_function: HarnessFunctionType = cookiecutter_harness_function


@dataclass
class CookieCutter4Tests4PyProject(Tests4PyProject):
    project: Project = api.cookiecutter_4
    grammar = project.grammar
    failing_inputs = [
        '{"full_name":"Marius Smytzek",'
        '"email":"mariussmtzek@cispa.de",'
        '"github_username":"smythi93",'
        '"project_name":"Test4Py Project",'
        '"repo_name":"t4p",'
        '"project_short_description":"The t4p project",'
        '"release_date":"2022-12-25","year":"2022","version":"0.1"}\n'
        "pre:echo,pre1\n"
        "pre:echo,pre2",
    ]
    passing_inputs = [
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
    harness_function: HarnessFunctionType = cookiecutter_harness_function


@dataclass
class FastAPI1Tests4PyProject(Tests4PyProject):
    project: Project = api.fastapi_1
    grammar = project.grammar
    initial_inputs = [
        "-o\"{'foo':'test'}\" -d",
        "-o\"{'foo':'test'}\"",
    ]


@dataclass
class YoutubeDL1Tests4PyProject(Tests4PyProject):
    project: Project = api.youtubedl_1
    grammar = grammar_youtube_dl_1
    initial_inputs = [
        "-q '!like_count' -d {'dislike_count': 85}",
        "-q '!is_live' -d {'is_live': False}",
        "-q 'test >? 0' -d {}",
    ]


@dataclass
class Middle1Tests4PyProject(Tests4PyProject):
    project: Project = api.middle_1
    grammar = project.grammar
    initial_inputs = ["4 2 5", "2 4 5"]


@dataclass
class Middle2Tests4PyProject(Tests4PyProject):
    project: Project = api.middle_2
    grammar = project.grammar
    initial_inputs = ["4 2 5", "2 4 5"]


@dataclass
class CalculatorTests4PyProject(Tests4PyProject):
    project: Project = api.calculator_1
    grammar = project.grammar
    initial_inputs = [
        "cos(-900)",
        "sqrt(-100)",
    ]


@dataclass
class ExpressionTests4PyProject(Tests4PyProject):
    project: Project = api.expression_1
    grammar = project.grammar
    failing_inputs = ["(3 * 5) / 0"]
    passing_inputs = [
        "23 + 45",
    ]


@dataclass
class Markup1Tests4PyProject(Tests4PyProject):
    project: Project = api.markup_1
    grammar = project.grammar
    initial_inputs = [
        "<zmcytjrhdd>IbXMFocpXLguFvGtxEqZxmH</zmcytjrhdd>",
        '\\"\\"cecpQLBVBzDVeycWLgrjTJhqa\\"\\"',
    ]
    harness_function: HarnessFunctionType = markup_harness_function


@dataclass
class Markup2Tests4PyProject(Tests4PyProject):
    project: Project = api.markup_2
    grammar = project.grammar
    initial_inputs = [
        "<pnufclccpw>kojZEXvCqkEZHkfRAZxS</pnufclccpw>",
        '\\"\\"cecpQLBVBzDVeycWLgrjTJhqa\\"\\"',
    ]
    harness_function: HarnessFunctionType = markup_harness_function

    def __post_init__(self):
        super().__init__(
            self.project,
            self.grammar,
            self.failing_inputs,
            self.passing_inputs,
            self.harness_function,
        )


if __name__ == "__main__":
    pro = CookieCutter2Tests4PyProject()
    print(pro.grammar)
