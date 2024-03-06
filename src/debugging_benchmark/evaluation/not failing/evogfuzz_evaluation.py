from evogfuzz.evogfuzz_class import EvoGFuzz
from debugging_benchmark.refactory import *
from debugging_benchmark.student_assignments import *
#from debugging_benchmark.tests4py_benchmark import *
from debugging_framework.tools import *
from debugging_framework.evaluator import Evaluation

student_repos = [
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

refactory_repos = [
        Question1RefactoryBenchmarkRepository(),
        Question2aRefactoryBenchmarkRepository(),
        Question2bRefactoryBenchmarkRepository(),
        Question2cRefactoryBenchmarkRepository(),
        Question3RefactoryBenchmarkRepository(),
        Question4RefactoryBenchmarkRepository(),
        Question5RefactoryBenchmarkRepository()
    ]

def evogfuzz(repo: BenchmarkRepository):
    subjects = []
    programs = repo.build()
    # 1 StudentAssignment gleich 10 Programme
    for program in programs:
        subjects.append(program)


    for subject in subjects:
        out_file = "evogfuzz_" + subject.name
        evogfuzz_eval = Evaluation([EvoGFuzzEvaluationFuzzer], [subject], 10, 3600)
        df = evogfuzz_eval.run()
        evogfuzz_eval.export_to_latex(df, out_file)

def main():
    evogfuzz(NPrStudentAssignmentBenchmarkRepository())
    







if __name__ == "__main__":
    main()