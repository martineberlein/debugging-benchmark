import unittest

from fuzzingbook.Parser import EarleyParser, tree_to_string, is_valid_grammar
from debugging_framework.oracle import OracleResult
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository, CalculatorBenchmarkProgram


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.repo = CalculatorBenchmarkRepository()
        self.program = self.repo.build().pop()
        
    def test_build(self):
        self.assertIsInstance(self.program, CalculatorBenchmarkProgram)

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
            self.assertEqual(oracle(inp), expected_result)


if __name__ == "__main__":
    unittest.main()
