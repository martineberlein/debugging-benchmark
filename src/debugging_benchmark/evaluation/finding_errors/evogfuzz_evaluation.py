from debugging_benchmark.refactory import *
from debugging_benchmark.student_assignments import *
#from debugging_benchmark.tests4py_benchmark import *
from debugging_framework.tools import *
from debugging_framework.evaluator import Evaluation
from debugging_framework.oracle import OracleResult

student_repos = [
        NPrStudentAssignmentBenchmarkRepository,
        SquareRootAssignmentBenchmarkRepository,
        GCDStudentAssignmentBenchmarkRepository,
        SieveOfEratosthenesStudentAssignmentBenchmarkRepository,
        MiddleAssignmentBenchmarkRepository,
        FibonacciStudentAssignmentBenchmarkRepository,
        BubbleSortAssignmentBenchmarkRepository,
        PalindromeAssignmentBenchmarkRepository,
        RemoveVowelAssignmentBenchmarkRepository,
        MergeStringsAssignmentBenchmarkRepository
    ]

refactory_repos = [
        Question1RefactoryBenchmarkRepository,
        Question2aRefactoryBenchmarkRepository,
        Question2bRefactoryBenchmarkRepository,
        Question2cRefactoryBenchmarkRepository,
        Question3RefactoryBenchmarkRepository,
        Question4RefactoryBenchmarkRepository,
        Question5RefactoryBenchmarkRepository
    ]

def eval_repo_evogfuzz_kai(repo: BenchmarkRepository):
    subjects = repo().build()
    repo_name = repo.name
    for subject in subjects:
        subject_name = subject.get_name()
        grammar = subject.get_grammar()
        oracle = subject.get_oracle()
        init_inputs = subject.get_initial_inputs()
        passing_inputs = [inp for inp in init_inputs if(oracle(inp) == (OracleResult.PASSING, None))]
        if passing_inputs:
            evo = EvoGFuzz(grammar, oracle, passing_inputs)
            evo.fuzz()
            gen_inputs = evo.get_all_inputs()
            failing_inputs = evo.get_found_exceptions_inputs()
            file = "evogfuzz_" + repo_name.lower() + ".txt"
            with open(file, "a") as f:
                f.write(subject_name + "\n")
                f.write("All Inputs: " + str(len(gen_inputs)) + "\n")
                f.write("Failing Inputs: " + str(len(failing_inputs)) + "\n\n")

def eval_repo_evogfuzz_with_evaluator(repo: BenchmarkRepository):
    subjects = repo().build()
    eval = Evaluation(InputsFromHellEvaluationFuzzer, subjects, 1)
    eval.export_to_latex(eval.run(), "evogfuzz_" + repo.name.lower())

def eval_repo_tool_with_evaluator(repo: BenchmarkRepository, tool: Tool, reps: int):
    subjects = repo().build()
    eval = Evaluation(tool, subjects, reps)
    df = eval.run()
    eval.export_to_latex(df, tool.name.lower() + "_" +  repo.name.lower())

def main():
    #eval_repo_evogfuzz_with_evaluator(MiddleAssignmentBenchmarkRepository)
    eval_repo_tool_with_evaluator(MiddleAssignmentBenchmarkRepository, InputsFromHellEvaluationFuzzer, 2)



if __name__ == "__main__":
    main()