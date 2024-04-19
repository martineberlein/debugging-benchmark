import unittest

import pandas as pd

from debugging_framework.evaluation.evaluator import Evaluation
from debugging_benchmark.student_assignments.repository import (
    GCDStudentAssignmentRepository,
)
from debugging_framework.evaluation.tools import InputsFromHellEvaluationFuzzer


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.tools = [
            InputsFromHellEvaluationFuzzer,
        ]

        self.subjects = (
            GCDStudentAssignmentRepository().build()
        )

    def test_evaluation(self):
        result = Evaluation(
            tool=self.tools[0], subjects=self.subjects[0:1], repetitions=1
        ).run()
        self.assertTrue(isinstance(result, pd.DataFrame))


if __name__ == "__main__":
    unittest.main()
