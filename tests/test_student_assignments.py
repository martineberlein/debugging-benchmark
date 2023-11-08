import unittest

from fuzzingbook.Grammars import is_valid_grammar

from debugging_framework.oracle import OracleResult
from debugging_benchmark.student_assignments import (
    MPITestSubjectFactory,
    SieveOfEratosthenesTestSubject,
    MiddleTestSubject,
    SquareRootTestSubject,
    GCDTestSubject,
    NPrTestSubject,
    FibonacciTestSubject,
    BubbleSortTestSubject,
    PalindromeTestSubject,
    RemoveVowelTestSubject,
    MergeStringsTestSubject
)


class TestStudentAssignments(unittest.TestCase):
    def setUp(self):
        self.subjects = [
            NPrTestSubject,
            SquareRootTestSubject,
            GCDTestSubject,
            SieveOfEratosthenesTestSubject,
            MiddleTestSubject,
            FibonacciTestSubject,
            BubbleSortTestSubject,
            PalindromeTestSubject,
            RemoveVowelTestSubject,
            MergeStringsTestSubject
        ]

    def test_subject_grammars(self):
        for subject in self.subjects:
            self.assertTrue(is_valid_grammar(subject.default_grammar))

    def test_build_subjects(self):
        subjects = MPITestSubjectFactory(self.subjects).build()

        for subject in subjects:
            # in case of failure ontinues and outputs all failures at the end
            with self.subTest(subject):
                # print(f"{subject.name} Subject {subject.id}")
                param = subject.to_dict()
                oracle = param.get("oracle")
                for inp in param.get("initial_inputs"):
                    result, opt_excp = oracle(inp)
                    self.assertIsInstance(result, OracleResult)
                    # self.assertEqual(subject.id % 2, 0)
                    # print(f"inp: {inp} | result: {result}")


if __name__ == "__main__":
    unittest.main()
