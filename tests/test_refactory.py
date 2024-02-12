import unittest

from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.GrammarFuzzer import tree_to_string

from debugging_benchmark.refactory import *


def check_directory_exists(path):
    return os.path.isdir(path)


class TestRefactory(unittest.TestCase):
    def setUp(self):
        self.repos = [
            Question1RefactoryBenchmarkRepository(),
            Question2aRefactoryBenchmarkRepository(),
            Question2bRefactoryBenchmarkRepository(),
            Question2cRefactoryBenchmarkRepository(),
            Question3RefactoryBenchmarkRepository(),
            Question4RefactoryBenchmarkRepository(),
            Question5RefactoryBenchmarkRepository()
        ]
        #if .build() fails all testcases fail but saves computing
        self.refactorys = []
        for repo in self.repos:
            refactorys = repo.build()
            for refactory in refactorys:
                self.assertTrue(isinstance(refactory, RefactoryBenchmarkProgram))
                self.refactorys.append(refactory)

    def test_get_dir(self):
        for repo in self.repos:
            self.assertTrue(check_directory_exists(repo.get_dir()))
    
    def test_valid_grammar(self):
        for repo in self.repos:
            self.assertTrue(is_valid_grammar(repo.get_grammar()))
    
    def test_subject_parsing_inputs(self):
                
        for refactory in self.refactorys:
            with self.subTest(refactory):
                self.assertTrue(isinstance(refactory, RefactoryBenchmarkProgram))
                grammar = refactory.get_grammar()
                parser = EarleyParser(grammar)

                for inp in refactory.get_initial_inputs():
                    self.assertIsNotNone(parser.parse(inp))
                    for tree in parser.parse(inp):
                        self.assertEqual(inp, tree_to_string(tree))


if __name__ == "__main__":
    unittest.main()
