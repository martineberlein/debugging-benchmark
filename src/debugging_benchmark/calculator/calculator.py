import math
from typing import Union, Callable, List
import string

from fuzzingbook.Grammars import Grammar

from debugging_framework.oracle import OracleResult
from debugging_framework.input import Input
from debugging_framework.benchmark import BenchmarkProgram


class CalculatorBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        initial_inputs: List[str],
        oracle: Callable,
    ):
        super().__init__(name, grammar, oracle)
        self.bug_id = bug_id
        self.initial_inputs = initial_inputs

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

#tried to stick to the design concept, but calculator is missing some key features
#so we further broke it down
class CalculatorBenchmarkRepository():
    def __init__(self):
        self.name = "Calculator"
        self.bug_id = 1
        self.grammar: Grammar = {
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
        self.initial_inputs = ["cos(12)", "sqrt(-900)"]

    def build(self) -> CalculatorBenchmarkProgram:
        return CalculatorBenchmarkProgram(
            self.name,
            self.bug_id,
            self.grammar,
            self.initial_inputs,
            self.oracle)

    def arith_eval(self, inp: Union[Input, str]) -> float:
        return eval(
            str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
        )

    def oracle(self, inp: Union[Input, str]) -> OracleResult:
        try:
            self.arith_eval(inp)
        except ValueError:
            return OracleResult.FAILING
        return OracleResult.PASSING
