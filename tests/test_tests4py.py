import unittest
from typing import Union

from fuzzingbook.GrammarFuzzer import GrammarFuzzer, is_valid_grammar
from fuzzingbook.Parser import EarleyParser, tree_to_string

from debugging_framework.oracle import OracleResult
from debugging_benchmark.tests4py_benchmark import PysnooperBenchmarkRepository, YoutubeDLBenchmarkRepository


class TestTests4Py(unittest.TestCase):

    def setUp(self):
        repositories = [
            # PysnooperBenchmarkRepository(),
            YoutubeDLBenchmarkRepository()
        ]
        self.subjects = []
        for repo in repositories:
            subjects = repo.build()
            for subject in subjects:
                self.subjects.append(subject)

        print(self.subjects)

    def test_tests4py_valid_grammars(self):
        for subject in self.subjects:
            self.assertTrue(is_valid_grammar(subject.grammar))

    def test_tests4py_initial_inputs_parsing(self):
        for subject in self.subjects:
            parser = EarleyParser(subject.grammar)
            for inp in subject.initial_inputs:
                for tree in parser.parse(inp):
                    self.assertEqual(inp, tree_to_string(tree))

    def test_tests4py_input_generation(self):
        for subject in self.subjects:
            fuzzer = GrammarFuzzer(subject.grammar)
            for _ in range(100):
                print("---")
                inp = fuzzer.fuzz()
                print(inp, subject.oracle(inp))

    def test_tests4py_verify_oracle(self):
        for subject in self.subjects:
            for inp in subject.initial_inputs:
                oracle, exception = subject.oracle(inp)
                self.assertIsInstance(oracle, OracleResult)
                self.assertIsInstance(exception, Union[Exception, None])


if __name__ == '__main__':
    unittest.main()
