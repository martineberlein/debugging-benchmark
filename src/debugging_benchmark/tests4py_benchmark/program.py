from typing import List

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.fuzzingbook.grammar import Grammar
from debugging_framework.types import OracleType


class Tests4PyBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        failing_inputs: List[str],
        passing_inputs: List[str],
        oracle: OracleType,
    ):
        super().__init__(name, grammar, oracle, failing_inputs, passing_inputs)
        self.bug_id = bug_id

    def __repr__(self):
        return f"Tests4PyBenchmarkProgram({self.name}_{self.bug_id})"
