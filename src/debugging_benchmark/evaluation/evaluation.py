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

def eval_latex(repo: BenchmarkRepository, tool: Tool, reps: int):
    subjects = repo().build()
    eval = Evaluation(tool, subjects, reps)
    df = eval.run()
    #TODO: Path anpassen
    eval.export_to_latex(df, tool.name.lower() + "_" +  repo().name.lower())

def eval_pickle(repo: BenchmarkRepository, tool: Tool, reps: int):
    subjects = repo().build()
    for subject in subjects:
        name = subject.get_name()
        inputs = subject.get_initial_inputs()
        oracle = subject.get_oracle()
        
        for inp in inputs:
            print(name, inp, oracle(inp))
    eval = Evaluation(tool, subjects, reps)
    df = eval.run()

    #if tool == EvoGFuzzEvaluationFuzzer:
    #    tool_folder = "evogfuzz"
    #elif tool == InputsFromHellEvaluationFuzzer:
    #    tool_folder = "inputsfromhell"
    #elif tool == GrammarBasedEvaluationFuzzer:
    #    tool_folder = "random"
    #elif tool == EvoGGenEvaluationFuzzer:
    #    tool_folder = "evoggen"
    #else:
    #    raise ValueError("Tool not supported")
    
    #file_path = "src/debugging_benchmark/evaluation/" + tool_folder + "/" + tool.name.lower() + "_" + repo().name.lower() + ".pkl"
    #df.to_pickle(file_path)

def run_evals():
    for tool in tools:
        for repo in repos:
            reps = 1 if tool == EvoGFuzzEvaluationFuzzer else 10
            eval_pickle(repo, tool, reps)

#def pickle_to_eval(path):

def main():
    #run_evals()
    #does something different on 8,9,10???
    #eval_pickle(GCDStudentAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #killed on 2????
    #eval_pickle(SieveOfEratosthenesStudentAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #funktioniert 1-10 mit dem oracle?? wieso dann GCD nicht???
    #eval_pickle(NPrStudentAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #same as npr good
    #eval_pickle(FibonacciStudentAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #auch good
    #eval_pickle(NumberOfDivisorsAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #laut oracle für bubble 2, 3, 4 ,5,6,7,8,9 (1 und 10 haben failing inputs)
    #auffällig entweder alle inputs failing oder passing
    #eval_pickle(BubbleSortAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #looks good
    #eval_pickle(MiddleAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #fehlermeldung bisschen weird to many positional arguments .. harness function falsch??
    eval_pickle(PalindromeAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #same wie palindrome muss ander harness function liegen??
    #eval_pickle(RemoveVowelAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #looks good
    #eval_pickle(SquareRootAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)
    #wtf???
    #eval_pickle(MergeStringsAssignmentBenchmarkRepository, EvoGGenEvaluationFuzzer, 1)

if __name__ == "__main__":
    main()

