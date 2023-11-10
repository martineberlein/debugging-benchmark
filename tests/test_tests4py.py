import unittest

from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.Parser import EarleyParser, tree_to_string

from debugging_framework.oracle import OracleResult
from debugging_benchmark.tests4py_benchmark import PysnooperBenchmarkRepository


class TestTests4Py(unittest.TestCase):

    def setUp(self):
        repo = PysnooperBenchmarkRepository()
        self.subjects = repo.build()

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

    def test_tests4py_build(self):
        for subject in self.subjects:
            for inp in subject.initial_inputs:
                oracle = subject.oracle
                print(inp, oracle)
                self.assertIsInstance(oracle(inp), OracleResult)


if __name__ == '__main__':
    unittest.main()
