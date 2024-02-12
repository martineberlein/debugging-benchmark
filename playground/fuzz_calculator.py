from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.tools import GrammarBasedEvaluationFuzzer


def main():
    calculator_repo = CalculatorBenchmarkRepository()
    calculator_subjects = calculator_repo.build()

    print(f"Fuzzing the calculator repository ({calculator_repo})...")

    for calculator_subject in calculator_subjects:
        print(f"Fuzzing the calculator subject ({calculator_subject})...")

        param = calculator_subject.to_dict()

        fuzzer = GrammarBasedEvaluationFuzzer(**param)
        failing_inputs = fuzzer.run().get_all_failing_inputs()

        print(f"Found the following failing inputs:")
        for failing_input in failing_inputs:
            print(failing_input)


if __name__ == "__main__":
    main()
