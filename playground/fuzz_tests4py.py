from typing import List, Type
import logging

from debugging_benchmark.tests4py_benchmark import (
    PysnooperBenchmarkRepository,
    BenchmarkRepository
)

from debugging_framework.tools import Tool
from debugging_framework.evaluator import Evaluation

from debugging_framework.tools import InputsFromHellEvaluationFuzzer


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:  %(message)s")

    tools: List[Type[Tool]] = [
        InputsFromHellEvaluationFuzzer,
        # EvoGFuzzEvaluationTool
    ]

    subjects = PysnooperBenchmarkRepository().build()

    report = Evaluation(tools=tools, subjects=subjects, repetitions=1, timeout=3600).run()

    print(report)


if __name__ == "__main__":
    exit(main())
