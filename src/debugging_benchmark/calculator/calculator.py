import math
from typing import Union, Callable, List, Dict
import string

from debugging_framework.types import Grammar
from debugging_framework.input.oracle import OracleResult
from debugging_framework.input.input import Input
from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository


def arith_eval(inp: Union[Input, str]) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    )


def calculator_oracle(inp: Union[Input, str]) -> OracleResult:
    try:
        arith_eval(inp)
    except ValueError:
        return OracleResult.FAILING
    return OracleResult.PASSING


calculator_grammar: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><one_nine><maybe_digits><maybe_frac>"],
    "<maybe_minus>": ["", "-"],
    "<maybe_frac>": ["", ".<digits>"],
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": [digit for digit in string.digits],
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


calculator_initial_inputs = ["cos(12)", "sqrt(-900)"]


class CalculatorBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        failing_inputs: List[str],
        passing_inputs: List[str],
        oracle: Callable,
    ):
        super().__init__(name, grammar, oracle, failing_inputs, passing_inputs)
        self.bug_id = bug_id

    def __repr__(self):
        return f"Calculator{self.name}_{self.bug_id}"


class CalculatorBenchmarkRepository(BenchmarkRepository):

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        return [
            CalculatorBenchmarkProgram(
                name="Calculator",
                bug_id=1,
                grammar=calculator_grammar,
                oracle=calculator_oracle,
                failing_inputs=["sqrt(-900)"],
                passing_inputs=["cos(10)"]
            )
        ]
