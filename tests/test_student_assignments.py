import unittest
from typing import List

from isla.parser import EarleyParser

from debugging_framework.fuzzingbook.grammar import is_valid_grammar
from debugging_framework.fuzzingbook.helper import tree_to_string
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.student_assignments.repository import (
    StudentAssignmentBenchmarkProgram,
    StudentAssignmentRepository,
    GCDStudentAssignmentRepository,
    SieveOfEratosthenesStudentAssignmentRepository,
    NPrStudentAssignmentRepository,
    FibonacciStudentAssignmentRepository,
    BubbleSortStudentAssignmentRepository,
    NumberOfDivisorsStudentAssignmentRepository,
    # SquareRootAssignmentBenchmarkRepository,
    # MiddleAssignmentBenchmarkRepository,
    # PalindromeAssignmentBenchmarkRepository,
    # RemoveVowelAssignmentBenchmarkRepository,
    # MergeStringsAssignmentBenchmarkRepository,
)


class TestStudentAssignments(unittest.TestCase):
    repos: List[StudentAssignmentRepository]
    programs: List[StudentAssignmentBenchmarkProgram]

    @classmethod
    def setUpClass(cls):
        cls.repos = [
            GCDStudentAssignmentRepository(),
            NPrStudentAssignmentRepository(),
            # SquareRootAssignmentBenchmarkRepository(),
            SieveOfEratosthenesStudentAssignmentRepository(),
            NumberOfDivisorsStudentAssignmentRepository(),
            # MiddleAssignmentBenchmarkRepository(),
            FibonacciStudentAssignmentRepository(),
            BubbleSortStudentAssignmentRepository(),
            # PalindromeAssignmentBenchmarkRepository(),
            # RemoveVowelAssignmentBenchmarkRepository(),
            # MergeStringsAssignmentBenchmarkRepository(),
        ]
        # if .build() fails all testcases fail but saves computing
        cls.programs = []
        for repo in cls.repos:
            programs = repo.build()
            for program in programs:
                cls.programs.append(program)

    def test_build(self):
        for program in self.programs:
            self.assertTrue(isinstance(program, StudentAssignmentBenchmarkProgram))
        self.assertNotEqual(len(self.programs), 0)

    def test_subject_valid_grammars(self):
        for program in self.programs:
            self.assertTrue(is_valid_grammar(program.get_grammar()))

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
