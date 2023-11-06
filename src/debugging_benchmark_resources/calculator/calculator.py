import math
from typing import Union
import string

from fuzzingbook.Grammars import Grammar

from debugging_benchmark.oracle import OracleResult
from debugging_benchmark.input import Input


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
    "<number>": ["<maybe_minus><onenine><maybe_digits>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


initial_inputs = ["cos(12)", "sqrt(-900)"]
