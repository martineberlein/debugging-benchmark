import unittest

from fuzzingbook.Grammars import is_valid_grammar
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.GrammarFuzzer import tree_to_string

from debugging_framework.oracle import OracleResult
from debugging_benchmark.student_assignments import (
    NPrStudentAssignmentBenchmarkRepository,
    SquareRootAssignmentBenchmarkRepository,
    GCDStudentAssignmentBenchmarkRepository,
    SieveOfEratosthenesStudentAssignmentBenchmarkRepository,
    MiddleAssignmentBenchmarkRepository,
    FibonacciStudentAssignmentBenchmarkRepository,
    BubbleSortAssignmentBenchmarkRepository,
    PalindromeAssignmentBenchmarkRepository,
    RemoveVowelAssignmentBenchmarkRepository,
    MergeStringsAssignmentBenchmarkRepository,
    StudentAssignmentBenchmarkProgram
)


class TestStudentAssignments(unittest.TestCase):
    def setUp(self):
        self.repos = [
            NPrStudentAssignmentBenchmarkRepository(),
            SquareRootAssignmentBenchmarkRepository(),
            GCDStudentAssignmentBenchmarkRepository(),
            SieveOfEratosthenesStudentAssignmentBenchmarkRepository(),
            MiddleAssignmentBenchmarkRepository(),
            FibonacciStudentAssignmentBenchmarkRepository(),
            BubbleSortAssignmentBenchmarkRepository(),
            PalindromeAssignmentBenchmarkRepository(),
            RemoveVowelAssignmentBenchmarkRepository(),
            MergeStringsAssignmentBenchmarkRepository()
        ]
        #if .build() fails all testcases fail but saves computing
        self.programs = []
        for repo in self.repos:
            programs = repo.build()
            for program in programs:
                self.assertTrue(isinstance(program, StudentAssignmentBenchmarkProgram))
                self.programs.append(program)

    def test_build_NPr(self):
        repo = NPrStudentAssignmentBenchmarkRepository()
        programs = repo.build()
        for program in programs:
            self.assertTrue(isinstance(program, StudentAssignmentBenchmarkProgram))
 
    def test_subject_valid_grammars(self):
        for repos in self.repos:
            self.assertTrue(is_valid_grammar(repos.get_grammar()))

    def test_subject_parsing_inputs(self):
                
        for program in self.programs:
            with self.subTest(program):
                self.assertTrue(isinstance(program, StudentAssignmentBenchmarkProgram))
                grammar = program.get_grammar()
                parser = EarleyParser(grammar)

                for inp in program.get_initial_inputs():
                    self.assertIsNotNone(parser.parse(inp))
                    for tree in parser.parse(inp):
                        self.assertEqual(inp, tree_to_string(tree))

    def test_subject_build(self):
        for program in self.programs:
            with self.subTest(program):
                oracle = program.get_oracle()
                for inp in program.get_initial_inputs():
                    result, opt_excp = oracle(inp)
                    self.assertIsInstance(result, OracleResult)


if __name__ == "__main__":
    unittest.main()
