import math
from pathlib import Path
from typing import Union, Callable, List
import string

from fuzzingbook.Grammars import Grammar

from debugging_framework.oracle import OracleResult
from debugging_framework.input import Input
from debugging_framework.benchmark import BenchmarkProgram, BenchmarkRepository


def arith_eval(inp: Union[Input, str]) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    )


def oracle(inp: Union[Input, str]) -> OracleResult:
    try:
        arith_eval(inp)
    except ValueError:
        return OracleResult.FAILING
    return OracleResult.PASSING


grammar: Grammar = {
        "<start>": ["<arith_expr>"],
        "<arith_expr>": ["<function>(<number>)"],
        "<function>": ["sqrt", "sin", "cos", "tan"],
        "<number>": ["<maybe_minus><one_nine><maybe_digits><maybe_frac>"],
        "<maybe_minus>": ["", "-"],
        "<maybe_frac>": ["", ".<digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }


initial_inputs = ["cos(12)", "sqrt(-900)"]


class CalculatorBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar_: Grammar,
        initial_inputs_: List[str],
        oracle_: Callable,
    ):
        super().__init__(name, grammar_, oracle_, initial_inputs_)
        self.bug_id = bug_id

    def __repr__(self):
        return f"{self.name}_{self.bug_id}"

    def get_name(self) -> str:
        return self.__repr__()

    def get_grammar(self):
        return self.grammar

    def get_initial_inputs(self):
        return self.initial_inputs

    def get_oracle(self):
        return self.oracle


class CalculatorBenchmarkRepository(BenchmarkRepository):

    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass

    def get_implementation_function_name(self):
        pass

    def get_dir(self) -> Path:
        pass

    def __init__(self):
        self.name = "Calculator"
        self.bug_id = 1

    def build(self) -> CalculatorBenchmarkProgram:
        return CalculatorBenchmarkProgram(
            self.name,
            self.bug_id,
            grammar,
            initial_inputs,
            oracle)
