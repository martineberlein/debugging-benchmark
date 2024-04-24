from typing import List, Callable, Union
import shlex
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from debugging_benchmark.tests4py_benchmark.grammars import grammar_pysnooper
from debugging_framework.types import Grammar
from debugging_framework.input.input import Input
from debugging_framework.types import HarnessFunctionType
from debugging_benchmark.tests4py_benchmark.api import get_tests


def default_tests4py_api_harness_function(inp: Union[str, Input]) -> List[str]:
    parts = shlex.split(str(inp))
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


class Tests4PyProject:
    def __init__(
        self,
        project: Project,
        grammar: Grammar = None,
        failing_inputs: List[str] = None,
        passing_inputs: List[str] = None,
        harness_function: HarnessFunctionType = default_tests4py_api_harness_function,
    ):
        self.project = project
        self.grammar = grammar if grammar else project.grammar
        self.failing_inputs = (
            failing_inputs if failing_inputs else get_tests(project, failing=True)
        )
        self.passing_inputs = passing_inputs if passing_inputs else get_tests(project)
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
    def __init__(self):
        super().__init__(
            project=api.pysnooper_2,
            grammar=grammar_pysnooper,
            harness_function=pysnooper_harness_function,
            passing_inputs=[inp + " " for inp in get_tests(api.pysnooper_2)],
            failing_inputs=[
                inp + " " for inp in get_tests(api.pysnooper_2, failing=True)
            ],
        )


@dataclass
class Pysnooper3Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.pysnooper_3,
            grammar=grammar_pysnooper,
            harness_function=pysnooper_harness_function,
            passing_inputs=[inp + " " for inp in get_tests(api.pysnooper_3)],
            failing_inputs=[
                inp + " " for inp in get_tests(api.pysnooper_3, failing=True)
            ],
        )


@dataclass
class CookieCutter2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        project = api.cookiecutter_2
        super().__init__(
            project=project,
            harness_function=cookiecutter_harness_function,
        )


@dataclass
class CookieCutter3Tests4PyProject(Tests4PyProject):
    def __init__(self):
        project = api.cookiecutter_3
        super().__init__(
            project=project,
            harness_function=cookiecutter_harness_function,
        )


@dataclass
class CookieCutter4Tests4PyProject(Tests4PyProject):
    def __init__(self):
        project = api.cookiecutter_4
        super().__init__(
            project=project,
            harness_function=cookiecutter_harness_function,
        )


@dataclass
class FastAPI1Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.fastapi_1,
        )


@dataclass
class FastAPI2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.fastapi_2,
        )


@dataclass
class FastAPI3Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.fastapi_3,
        )


@dataclass
class Middle1Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.middle_1,
        )


@dataclass
class Middle2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.middle_2,
        )


@dataclass
class CalculatorTests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.calculator_1,
        )


@dataclass
class ExpressionTests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.expression_1,
        )


@dataclass
class Markup1Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(project=api.markup_1, harness_function=markup_harness_function)


@dataclass
class Markup2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(project=api.markup_2, harness_function=markup_harness_function)


@dataclass
class HTTPie1Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.httpie_1,
        )


@dataclass
class HTTPie2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.httpie_2,
        )


@dataclass
class Sanic1Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.sanic_1,
        )


@dataclass
class Sanic2Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.sanic_2,
        )


@dataclass
class Sanic3Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.sanic_3,
        )


@dataclass
class Sanic4Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.sanic_4,
        )


@dataclass
class Sanic5Tests4PyProject(Tests4PyProject):
    def __init__(self):
        super().__init__(
            project=api.sanic_5,
        )


if __name__ == "__main__":
    pro = CookieCutter2Tests4PyProject()
    print(pro.grammar)
