from typing import List

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.fuzzingbook.grammar import Grammar
from debugging_framework.types import OracleType


class StudentAssignmentBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        grammar: Grammar,
        failing_inputs: List[str],
        passing_inputs: List[str],
        oracle: OracleType,
    ):
        super().__init__(name, grammar, oracle, failing_inputs, passing_inputs)

    def __repr__(self):
        return f"StudentAssignmentBenchmarkProgram({self.name})"
