import unittest

from fuzzingbook.Parser import EarleyParser, tree_to_string, is_valid_grammar
from debugging_framework.oracle import OracleResult
from debugging_benchmark.calculator.calculator import grammar, initial_inputs, oracle


class TestCalculator(unittest.TestCase):
    def test_calculator_grammar(self):
        self.assertTrue(is_valid_grammar(grammar))

    def test_calculator_initial_inputs(self):
        parser = EarleyParser(grammar)

        for inp in initial_inputs:
            for tree in parser.parse(inp):
                self.assertEqual(inp, tree_to_string(tree))

    def test_calculator_oracle(self):
        inputs = [
            ("sqrt(-900)", OracleResult.FAILING),
            ("cos(10)", OracleResult.PASSING),
        ]

        for inp, expected_result in inputs:
            self.assertEqual(oracle(inp), expected_result)


if __name__ == "__main__":
    unittest.main()
