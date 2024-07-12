from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer
from debugging_framework.benchmark.program import BenchmarkProgram
from tests4py.api.logging import deactivate, debug


if __name__ == "__main__":
    deactivate()
    # debug()

    benchmark_program: BenchmarkProgram = BenchmarkProgram.load("./benchmark_program.pickle")

    fuzzer = GrammarFuzzer(benchmark_program.get_grammar())
    oracle = benchmark_program.get_oracle()

    for inp in benchmark_program.get_initial_inputs():
        print(f"Input: {inp}, Oracle: {oracle(inp)}")

    for i in range(10):
        inp = fuzzer.fuzz()
        print(f"Input: {inp}, Oracle: {oracle(inp)}")

