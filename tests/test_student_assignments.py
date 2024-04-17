import unittest

from isla.parser import EarleyParser

from debugging_framework.fuzzingbook.grammar import is_valid_grammar
from debugging_framework.fuzzingbook.helper import tree_to_string
from debugging_framework.input.oracle import OracleResult
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
    StudentAssignmentBenchmarkProgram,
    StudentAssignmentRepository,
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
            MergeStringsAssignmentBenchmarkRepository(),
        ]
        # if .build() fails all testcases fail but saves computing
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
        for repo in self.repos:
            repo: StudentAssignmentRepository
            self.assertTrue(is_valid_grammar(repo.get_grammar()))

    def test_subject_parsing_inputs(self):
        for program in self.programs:
            program: StudentAssignmentBenchmarkProgram
            self.assertTrue(isinstance(program, StudentAssignmentBenchmarkProgram))
            parser = EarleyParser(program.get_grammar())
            with self.subTest("Problem at " + program.get_name()):
                for inp in program.get_initial_inputs():
                    self.assertIsNotNone(parser.parse(inp))
                    for tree in parser.parse(inp):
                        self.assertEqual(inp, tree_to_string(tree))

    def test_failing_input(self):
        for program in self.programs:
            program: StudentAssignmentBenchmarkProgram
            oracle = program.get_oracle()
            print(program)
            for inp in program.get_failing_inputs():
                with self.subTest(
                    "Problem at " + program.get_name() + " and input " + inp
                ):
                    result, _ = oracle(inp)
                    self.assertIs(result, OracleResult.FAILING)

    def test_passing_input(self):
        for program in self.programs:
            program: StudentAssignmentBenchmarkProgram
            oracle = program.get_oracle()
            for inp in program.get_passing_inputs():
                with self.subTest(
                    "Problem at " + program.get_name() + " and input " + inp
                ):
                    result, _ = oracle(inp)
                    self.assertIs(result, OracleResult.PASSING)

    def test_subject_build(self):
        for program in self.programs:
            with self.subTest(program):
                oracle = program.get_oracle()
                for inp in program.get_initial_inputs():
                    result, _ = oracle(inp)
                    self.assertIsInstance(result, OracleResult)


if __name__ == "__main__":
    unittest.main()
