import unittest

import pandas as pd

from debugging_framework.evaluator import Evaluation
from debugging_benchmark.student_assignments import (
    SieveOfEratosthenesTestSubject,
    MPITestSubjectFactory,
)
from debugging_framework.tools import InputsFromHellEvaluationFuzzer


class TestEvaluator(unittest.TestCase):
    def test_setup(self):
        tools = [
            InputsFromHellEvaluationFuzzer,
        ]

        subjects = MPITestSubjectFactory([SieveOfEratosthenesTestSubject]).build()

        result = Evaluation(
            tools=tools, subjects=subjects[0:1], repetitions=1, timeout=3600
        ).run()
        self.assertTrue(isinstance(result, pd.DataFrame))


if __name__ == "__main__":
    unittest.main()
