from debugging_benchmark.refactory import (
    Question1RefactoryBenchmarkRepository,
    Question2bRefactoryBenchmarkRepository,
    Question2aRefactoryBenchmarkRepository,
    Question2cRefactoryBenchmarkRepository,
    Question3RefactoryBenchmarkRepository,
    Question4RefactoryBenchmarkRepository,
    Question5RefactoryBenchmarkRepository,
)

from fuzzingbook.GrammarFuzzer import GrammarFuzzer


def main():
    refactory_repos = [
        Question1RefactoryBenchmarkRepository(),
        Question2aRefactoryBenchmarkRepository(),
        Question2bRefactoryBenchmarkRepository(),
        Question2cRefactoryBenchmarkRepository(),
        Question3RefactoryBenchmarkRepository(),
        Question4RefactoryBenchmarkRepository(),
        Question5RefactoryBenchmarkRepository(),
    ]

    for repo in refactory_repos:
        print(f"Fuzzing the refactory repository ({repo})...")

        subjects = repo.build()

        for subject in subjects:
            print(f"Fuzzing the {repo} subject ({subject})...")

            grammar = subject.get_grammar()
            fuzzer = GrammarFuzzer(grammar)
            print(fuzzer.fuzz())


if __name__ == "__main__":
    main()
