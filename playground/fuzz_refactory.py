from debugging_benchmark.refactory import (
    Question1RefactoryBenchmarkRepository,
    Question2bRefactoryBenchmarkRepository,
    Question2aRefactoryBenchmarkRepository,
    Question2cRefactoryBenchmarkRepository,
    Question3RefactoryBenchmarkRepository,
    Question4RefactoryBenchmarkRepository,
    Question5RefactoryBenchmarkRepository)

from fuzzingbook.GrammarFuzzer import GrammarFuzzer

def main():
    subjects = Question5RefactoryBenchmarkRepository().build()
    for subject in subjects:
        grammar = subject.get_grammar()
        fuzzer = GrammarFuzzer(grammar)
        print(fuzzer.fuzz())
    
    test = "24, (August, 22); (January, 4)"
    arg1, arg2 = Question2aRefactoryBenchmarkRepository().harness_function(test)
    print(arg1)
    print(arg2)


if __name__ == "__main__":
    main()
