import argparse

from debugging_framework.evaluator import Evaluation
from debugging_framework.tools import (GrammarBasedEvaluationFuzzer,
                                    InputsFromHellEvaluationFuzzer,
                                    ISLaGrammarEvaluationFuzzer)

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
    MergeStringsAssignmentBenchmarkRepository)

#TODO: Man könnte das erweitern mit allen Tools des Frameworks
#Dann entweder für jede Möglichkeit eine File und ein Keyword
#oder ein Keyword mit unterschiedlichen Optionen
#Aktuell nur Evaluation mit keyword evaluation

def main():
    parser = argparse.ArgumentParser(prog = "evaluation",
                                    description= "Test test test")

    parser.add_argument("subjects",
                     	help= "choose a specific subject\n"
                              "default is all\n"
                              "1 = NPr\n"
                              "2 = sqrt\n"
                              "3 = GCD\n"
                              "4 = SieveOfEratosthenes\n"
                              "5 = middle\n"
                              "6 = fibonacci\n"
                              "7 = bubble sort\n"
                              "8 = palindorome\n"
                              "9 = remove vowel\n"                              
                              "10 = merge strings",
                        default=0,
                        type=int)
    
    parser.add_argument("tools",
                        help= "choose a specific tool\n"
                              "default is all\n"
                              "1 = GrammarBasedFuzzer\n"
                              "2 = InputsFromHellFuzzer\n"
                              "3 = ISLAGrammarFuzzer",
                        default=0,
                        type=int)
      
    parser.add_argument("-r", "--repetitions",
                        help="Repititions of the Evaluation Tool. Default is 1.",
                        default=1,
                        type=int)
      
    parser.add_argument("-t", "--timeout",
                        help="Terminates if not finished after 3600 seconds",
                        default=3600,
                        type=int)
    
    args = parser.parse_args()
    
    match args.tools:
        case 1:
            tools = [GrammarBasedEvaluationFuzzer]
        case 2:
            tools = [InputsFromHellEvaluationFuzzer]
        case 3:
            tools = [ISLaGrammarEvaluationFuzzer]
        case 0:
            tools = [GrammarBasedEvaluationFuzzer,
                    InputsFromHellEvaluationFuzzer,
                    ISLaGrammarEvaluationFuzzer]
    
    match args.subjects:
        case 1:
            subjects = NPrStudentAssignmentBenchmarkRepository().build()
        case 2:
            subjects = SquareRootAssignmentBenchmarkRepository().build()
        case 3:
            subjects = GCDStudentAssignmentBenchmarkRepository().build()
        case 4:
            subjects = SieveOfEratosthenesStudentAssignmentBenchmarkRepository().build()
        case 5:
            subjects = MiddleAssignmentBenchmarkRepository().build()
        case 6:
            subjects = FibonacciStudentAssignmentBenchmarkRepository().build()
        case 7: 
            subjects = BubbleSortAssignmentBenchmarkRepository().build()
        case 8:
            subjects = PalindromeAssignmentBenchmarkRepository().build()
        case 9:
            subjects = RemoveVowelAssignmentBenchmarkRepository().build()
        case 10:
            subjects = MergeStringsAssignmentBenchmarkRepository().build()
        case 0:
            subjects = [
                NPrStudentAssignmentBenchmarkRepository().build(),
                SquareRootAssignmentBenchmarkRepository().build(),
                GCDStudentAssignmentBenchmarkRepository().build(),
                SieveOfEratosthenesStudentAssignmentBenchmarkRepository().build(),
                MiddleAssignmentBenchmarkRepository().build(),
                FibonacciStudentAssignmentBenchmarkRepository().build(),
                BubbleSortAssignmentBenchmarkRepository().build(),
                PalindromeAssignmentBenchmarkRepository().build(),
                RemoveVowelAssignmentBenchmarkRepository().build(),
                MergeStringsAssignmentBenchmarkRepository().build()
            ]
    
    evaluation = Evaluation(tools, subjects, args.repetitions, args.timeout).run()

    return evaluation



if __name__ == "__main__":
    exit(main())