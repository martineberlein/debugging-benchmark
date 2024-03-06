from debugging_framework.tools import EvoGFuzzEvaluationFuzzer

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

from debugging_benchmark.refactory import (
	Question1RefactoryBenchmarkRepository,
    Question2aRefactoryBenchmarkRepository,
    Question2bRefactoryBenchmarkRepository,
    Question2cRefactoryBenchmarkRepository,
    Question3RefactoryBenchmarkRepository,
    Question4RefactoryBenchmarkRepository,
    Question5RefactoryBenchmarkRepository
)

from debugging_benchmark.calculator import calculator
	

def main():
	tools = [EvoGFuzzEvaluationFuzzer]

	


if __name__ == "__main__":
	exit(main())