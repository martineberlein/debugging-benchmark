import sys
from typing import Dict, List, Union
import shlex
import string

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_framework.types import Grammar
from debugging_framework.input.input import Input
from debugging_framework.input.oracle_construction import FunctionalOracleConstructor

from .parse import parse


expression_grammar: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": [
        "<arith_expr><operator><arith_expr>",
        "<number>",
        "(<arith_expr>)",
    ],
    "<operator>": [" + ", " - ", " * ", " / "],
    "<number>": ["<maybe_minus><non_zero_digit><maybe_digits>", "0"],
    "<maybe_minus>": ["", "~ "],
    "<non_zero_digit>": [
        str(num) for num in range(1, 10)
    ],  # Exclude 0 from starting digits
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


def evaluate(inp: str | Input):
    term = parse(inp)
    result = term.evaluate()
    return result


def expression_oracle(inp: str | Input):
    return eval(str(inp).replace("~", "-"))


def expression_harness(inp: str | Input):
    return [str(inp)]


class ExpressionBenchmarkRepository(BenchmarkRepository):
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        oracle = FunctionalOracleConstructor(
            program=evaluate,
            program_oracle=expression_oracle,
            harness_function=expression_harness,
        ).build()

        return [
            BenchmarkProgram(
                name="expression",
                grammar=expression_grammar,
                oracle=oracle,
                failing_inputs=["1 / (1 - 1)", "9 / 0"],
                passing_inputs=[
                    "1 + 3",
                    "2 * 3",
                    "4 - 2",
                    "1 / 2",
                    "1 / 1",
                    "1 / 2 + 3",
                ],
            )
        ]


if __name__ == "__main__":
    prog = ExpressionBenchmarkRepository().build()[0]
    print(prog.oracle(prog.passing_inputs[0]))
