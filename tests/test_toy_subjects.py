import unittest
from typing import Union, List

from isla.parser import EarleyParser

from debugging_framework.fuzzingbook.grammar import is_valid_grammar
from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer
from debugging_framework.fuzzingbook.helper import tree_to_string
from debugging_framework.input.oracle import OracleResult
from debugging_framework.benchmark.program import BenchmarkProgram

from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_benchmark.middle.middle import MiddleBenchmarkRepository
from debugging_benchmark.expression.expression import ExpressionBenchmarkRepository


class TestToySubjects(unittest.TestCase):
    subjects: List[BenchmarkProgram]

    @classmethod
    def setUpClass(cls):
        repositories = [
            CalculatorBenchmarkRepository(),
            MiddleBenchmarkRepository(),
            ExpressionBenchmarkRepository()
        ]
        cls.subjects = []
        for repo in repositories:
            subjects = repo.build()
            for subject in subjects:
                cls.subjects.append(subject)
        assert len(cls.subjects) == 3

    def test_valid_grammars(self):
        for subject in self.subjects:
            self.assertTrue(is_valid_grammar(subject.grammar))

    def test_initial_inputs_parsing(self):
        for subject in self.subjects:
            parser = EarleyParser(subject.grammar)
            for inp in subject.get_initial_inputs():
                for tree in parser.parse(inp):
                    self.assertEqual(inp, tree_to_string(tree))

    def test_input_generation(self):
        for subject in self.subjects:
            fuzzer = GrammarFuzzer(subject.grammar)
            for _ in range(10):
                inp = fuzzer.fuzz()
                oracle, exception = subject.oracle(inp)
                self.assertIsInstance(oracle, OracleResult)
                self.assertIsInstance(exception, Union[Exception, None])

    def test_verify_passing_oracle(self):
        for subject in self.subjects:
            for inp in subject.get_passing_inputs():
                with self.subTest(subject=subject, input=inp):
                    oracle, exception = subject.oracle(inp)
                    self.assertIsInstance(oracle, OracleResult)
                    self.assertTrue(oracle == OracleResult.PASSING)
                    self.assertIs(exception, None)

    def test_verify_failing_oracle(self):
        for subject in self.subjects:
            for inp in subject.get_failing_inputs():
                with self.subTest(subject=subject, input=inp):
                    oracle, exception = subject.oracle(inp)
                    self.assertIsInstance(oracle, OracleResult)
                    self.assertEqual(oracle, OracleResult.FAILING)
                    self.assertIsInstance(exception, Exception)


if __name__ == "__main__":
    unittest.main()
