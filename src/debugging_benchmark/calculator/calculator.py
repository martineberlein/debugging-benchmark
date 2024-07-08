import math
from typing import Union, Callable, List, Dict, Tuple
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


def calculator_oracle(
    inp: Union[Input, str]
) -> Tuple[OracleResult, Union[Exception, None]]:
    try:
        arith_eval(inp)
    except ValueError:
        return OracleResult.FAILING, ValueError()
    return OracleResult.PASSING, None


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


calculator_grammar_with_zero: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><one_nine><maybe_digits><maybe_frac>", "-0", "0"],
    "<maybe_minus>": ["", "-"],
    "<maybe_frac>": ["", ".<digits>"],
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": [digit for digit in string.digits],
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


calculator_initial_inputs = ["cos(12)", "sqrt(-900)"]


class CalculatorBenchmarkRepository(BenchmarkRepository):
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        return [
            BenchmarkProgram(
                name="calculator",
                grammar=calculator_grammar,
                oracle=calculator_oracle,
                failing_inputs=["sqrt(-900)"],
                passing_inputs=["cos(10)"],
            )
        ]
