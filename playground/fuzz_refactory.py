from debugging_benchmark.refactory import Question1RefactoryBenchmarkRepository
from debugging_framework.tools import InputsFromHellEvaluationFuzzer


def main():
    subjects = Question1RefactoryBenchmarkRepository().build()
    for subject in subjects:
        param = subject.to_dict()
        print(InputsFromHellEvaluationFuzzer(**param).run())


if __name__ == "__main__":
    main()
