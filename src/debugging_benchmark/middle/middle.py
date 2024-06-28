from typing import Dict, List, Union
import shlex

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_framework.types import Grammar
from debugging_framework.input.input import Input
from debugging_framework.input.oracle_construction import FunctionalOracleConstructor

middle_grammar: Grammar = {
    "<start>": ["<x> <y> <z>"],
    "<x>": ["<integer>"],
    "<y>": ["<integer>"],
    "<z>": ["<integer>"],
    "<integer>": ["<integer_>", "-<integer_>"],
    "<integer_>": ["<digit>", "<digit><integer_>"],
    "<digit>": [str(num) for num in range(0, 10)],
}


def middle_harness(inp: Union[Input, str]):
    parts = shlex.split(str(inp))
    if parts and parts[-1] == "":
        parts.pop()
    return parts if parts else []


def middle_oracle(x, y, z):
    sorted_list = sorted([x, y, z])
    return sorted_list[1]


def middle(x, y, z):
    m = z
    if y < z:
        if x < y:
            m = y
        elif x < z:
            m = y
    else:
        if x > y:
            m = y
        elif x > z:
            m = x
    return m


class MiddleBenchmarkRepository(BenchmarkRepository):
    def build(
            self,
            err_def: Dict[Exception, OracleResult] = None,
            default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        oracle = FunctionalOracleConstructor(
            program=middle,
            program_oracle=middle_oracle,
            harness_function=middle_harness,
        ).build()

        return [BenchmarkProgram(
            name="middle",
            grammar=middle_grammar,
            oracle=oracle,
            failing_inputs=["4 2 5"],
            passing_inputs=["1 2 3", "3 2 1"],
        )]


if __name__ == "__main__":
    prog = MiddleBenchmarkRepository().build()[0]
    print(prog.oracle(prog.passing_inputs[1]))