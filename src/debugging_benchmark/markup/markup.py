from typing import Dict, List, Union
import shlex
import re

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_framework.types import Grammar
from debugging_framework.input.input import Input
from debugging_framework.input.oracle_construction import FunctionalOracleConstructor

from debugging_benchmark.tests4py_benchmark.grammars import grammar_markup

middle_grammar: Grammar = {
    "<start>": ["<x> <y> <z>"],
    "<x>": ["<integer>"],
    "<y>": ["<integer>"],
    "<z>": ["<integer>"],
    "<integer>": ["<integer_>", "-<integer_>"],
    "<integer_>": ["<digit>", "<digit><integer_>"],
    "<digit>": [str(num) for num in range(0, 10)],
}


def markup_harness(inp: Union[Input, str]):
    return [str(inp)]


def markup_oracle(s):
    pattern = re.compile("<[^<>]*>")
    expected = re.sub(pattern, "", s).strip()
    expected = expected.replace("^", "")
    return expected


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == "<" and not quote:
            tag = True
        elif c == ">" and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


class MarkupBenchmarkRepository(BenchmarkRepository):
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        oracle = FunctionalOracleConstructor(
            program=remove_html_markup,
            program_oracle=markup_oracle,
            harness_function=markup_harness,
        ).build()

        return [
            BenchmarkProgram(
                name="markup",
                grammar=grammar_markup,
                oracle=oracle,
                failing_inputs=['"abc"'],
                passing_inputs=["abc", "<b>abc</b>"],
            )
        ]


if __name__ == "__main__":
    prog = MarkupBenchmarkRepository().build()[0]
    print(prog.oracle(prog.passing_inputs[0]))
    print(prog.oracle(prog.failing_inputs[0]))
