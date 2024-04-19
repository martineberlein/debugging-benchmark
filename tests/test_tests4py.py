import unittest
from typing import Union, List

from isla.parser import EarleyParser

from debugging_framework.fuzzingbook.grammar import is_valid_grammar
from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer
from debugging_framework.fuzzingbook.helper import tree_to_string
from debugging_framework.input.oracle import OracleResult
from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_benchmark.tests4py_benchmark.repository import (
    PysnooperBenchmarkRepository,
    CookieCutterBenchmarkRepository,
    ToyExampleTests4PyBenchmarkRepository,
    CalculatorBenchmarkRepository
)


class TestTests4Py(unittest.TestCase):
    subjects: List[BenchmarkProgram]

    @classmethod
    def setUpClass(cls):
        repositories = [
            PysnooperBenchmarkRepository(),
            CookieCutterBenchmarkRepository(),
            ToyExampleTests4PyBenchmarkRepository(),
            # CalculatorBenchmarkRepository(),
        ]
        cls.subjects = []
        for repo in repositories:
            subjects = repo.build()
            for subject in subjects:
                cls.subjects.append(subject)

    def test_tests4py_valid_grammars(self):
        for subject in self.subjects:
            self.assertTrue(is_valid_grammar(subject.grammar))

    def test_tests4py_initial_inputs_parsing(self):
        for subject in self.subjects:
            parser = EarleyParser(subject.grammar)
            for inp in subject.get_initial_inputs():
                for tree in parser.parse(inp):
                    self.assertEqual(inp, tree_to_string(tree))

    def test_tests4py_input_generation(self):
        for subject in self.subjects:
            fuzzer = GrammarFuzzer(subject.grammar)
            print(subject.name)
            for _ in range(10):
                inp = fuzzer.fuzz()
                oracle, exception = subject.oracle(inp)
                self.assertIsInstance(oracle, OracleResult)
                self.assertIsInstance(exception, Union[Exception, None])

    def test_tests4py_verify_passing_oracle(self):
        for subject in self.subjects:
            for inp in subject.get_passing_inputs():
                with self.subTest(subject=subject, input=inp):
                    oracle, exception = subject.oracle(inp)
                    self.assertIsInstance(oracle, OracleResult)
                    self.assertTrue(oracle == OracleResult.PASSING)
                    self.assertIs(exception, None)

    def test_tests4py_verify_failing_oracle(self):
        for subject in self.subjects:
            for inp in subject.get_failing_inputs():
                with self.subTest(subject=subject, input=inp):
                    oracle, exception = subject.oracle(inp)
                    self.assertIsInstance(oracle, OracleResult)
                    self.assertEqual(oracle, OracleResult.FAILING)
                    self.assertIsInstance(exception, Exception)


if __name__ == "__main__":
    unittest.main()
