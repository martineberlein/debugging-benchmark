from debugging_benchmark.refactory import *
from debugging_benchmark.student_assignments import *
#from debugging_benchmark.tests4py_benchmark import *
from debugging_framework.tools import *
from debugging_framework.evaluator import Evaluation
from debugging_framework.oracle import OracleResult

tools = [
    EvoGFuzzEvaluationFuzzer,
    InputsFromHellEvaluationFuzzer,
    GrammarBasedEvaluationFuzzer, #random
    EvoGGenEvaluationFuzzer
]

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

repos = student_repos + refactory_repos

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

def eval_latex(repo: BenchmarkRepository, tool: Tool, reps: int):
    subjects = repo().build()
    eval = Evaluation(tool, subjects, reps)
    df = eval.run()
    #TODO: Path anpassen
    eval.export_to_latex(df, tool.name.lower() + "_" +  repo.name.lower())

def eval_pickle(repo: BenchmarkRepository, tool: Tool, reps: int):
    subjects = repo().build()
    eval = Evaluation(tool, subjects, reps)
    df = eval.run()

    if tool == EvoGFuzzEvaluationFuzzer:
        tool_folder = "evogfuzz"
    elif tool == InputsFromHellEvaluationFuzzer:
        tool_folder = "inputsfromhell"
    elif tool == GrammarBasedEvaluationFuzzer:
        tool_folder = "random"
    elif tool == EvoGGenEvaluationFuzzer:
        tool_folder = "evoggen"
    else:
        raise ValueError("Tool not supported")
    
    file_path = "src/debugging_benchmark/evaluation/" + tool_folder + "/" + tool.name.lower() + "_" + repo().name.lower() + ".pkl"
    df.to_pickle(file_path)

def run_evals():
    for tool in tools:
        for repo in repos:
            reps = 1 if tool == EvoGFuzzEvaluationFuzzer else 10
            eval_pickle(repo, tool, reps)

#def pickle_to_eval(path):

def main():
    #run_evals()
    #eval_latex(MiddleAssignmentBenchmarkRepository, EvoGFuzzEvaluationFuzzer, 1)
    #eval_pickle(MiddleAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    
if __name__ == "__main__":
    main()

