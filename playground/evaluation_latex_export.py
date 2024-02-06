from typing import List, Type

from debugging_benchmark.student_assignments import (
    NPrStudentAssignmentBenchmarkRepository,
)

from debugging_framework.tools import Tool
from debugging_framework.evaluator import Evaluation
from debugging_framework.tools import (
    InputsFromHellEvaluationFuzzer,
    GrammarBasedEvaluationFuzzer,
)


def main():
    tools: List[Type[Tool]] = [
        InputsFromHellEvaluationFuzzer,
        GrammarBasedEvaluationFuzzer,
    ]

    subjects = NPrStudentAssignmentBenchmarkRepository().build()

    evaluation = Evaluation(
        tools=tools,
        subjects=subjects,
        repetitions=1,
        timeout=3600,
        tool_param={"max_non_terminals": 8, "max_generated_inputs": 100},
    )
    report = evaluation.run()

    evaluation.export_to_latex(report, "Test.tex")
    print(evaluation.export_to_latex(report))


if __name__ == "__main__":
    exit(main())
