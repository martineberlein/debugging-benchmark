from typing import List, Callable, Union
import shlex
from dataclasses import dataclass

from tests4py import api
from tests4py.projects import Project

from debugging_framework.types import Grammar

from debugging_framework.input.input import Input
from debugging_framework.types import HARNESS_FUNCTION
from debugging_benchmark.tests4py.tests4py_grammars import (
    grammar_pysnooper,
    grammar_youtube_dl_1,
)


class Tests4PyProject:
    def __init__(
        self,
        project: Project,
        grammar: Grammar,
        failing_inputs: List[str],
        passing_inputs: List[str],
        harness_function: HARNESS_FUNCTION,
    ):
        self.project = project
        self.grammar = grammar
        self.failing_inputs = failing_inputs
        self.passing_inputs = passing_inputs
        self.harness_function: HARNESS_FUNCTION = harness_function
