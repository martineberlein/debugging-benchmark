import unittest

from debugging_framework.execution.report import Report
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.evaluation.tools import (
    GrammarBasedEvaluationFuzzer,
    InputsFromHellEvaluationFuzzer,
    ISLaGrammarEvaluationFuzzer,
)


class TestTools(unittest.TestCase):
    def setUp(self):
        calc = CalculatorBenchmarkRepository().build().pop()
        self.param = calc.to_dict()

    def test_grammar_based_evaluation_fuzzer(self):
        fuzzer = GrammarBasedEvaluationFuzzer(**self.param)
        report = fuzzer.run()
        self.assertTrue(isinstance(report, Report))

    def test_inputs_from_hell_fuzzer(self):
        fuzzer = InputsFromHellEvaluationFuzzer(**self.param)
        report = fuzzer.run()
        self.assertTrue(isinstance(report, Report))

    def test_isla_grammar_fuzzer(self):
        fuzzer = ISLaGrammarEvaluationFuzzer(**self.param)
        report = fuzzer.run()
        self.assertTrue(isinstance(report, Report))


if __name__ == "__main__":
    unittest.main()
