import unittest
import os

from isla.parser import EarleyParser

from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.fuzzingbook.grammar import is_valid_grammar
from debugging_framework.fuzzingbook.helper import tree_to_string
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.calculator.calculator import (
    CalculatorBenchmarkRepository,
)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.repo = CalculatorBenchmarkRepository()
        self.program = self.repo.build().pop()

    def test_build(self):
        self.assertIsInstance(self.program, BenchmarkProgram)

    def test_calculator_grammar(self):
        self.assertTrue(is_valid_grammar(self.program.get_grammar()))

    def test_calculator_initial_inputs(self):
        parser = EarleyParser(self.program.get_grammar())
        inputs = self.program.get_initial_inputs()

        for inp in inputs:
            for tree in parser.parse(inp):
                self.assertEqual(inp, tree_to_string(tree))

    def test_calculator_oracle(self):
        oracle = self.program.get_oracle()
        inputs = [
            ("sqrt(-900)", OracleResult.FAILING),
            ("cos(10)", OracleResult.PASSING),
        ]

        for inp, expected_result in inputs:
            result, _ = oracle(inp)
            self.assertEqual(result, expected_result)

    def test_dump_and_load(self):
        file = "./BenchmarkProgram.pickle"

        self.program.dump(file)
        program = BenchmarkProgram.load(file)
        self.assertEqual(program.get_name(), self.program.get_name())
        self.assertEqual(program.get_grammar(), self.program.get_grammar())
        self.assertEqual(program.get_oracle(), self.program.get_oracle())
        self.assertEqual(program.get_failing_inputs(), self.program.get_failing_inputs())
        self.assertEqual(program.get_passing_inputs(), self.program.get_passing_inputs())
        self.assertEqual(program.get_initial_inputs(), self.program.get_initial_inputs())
        if os.path.exists(file):
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
