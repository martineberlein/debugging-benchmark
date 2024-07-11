from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer

from debugging_benchmark.tests4py_benchmark.grammars import grammar_pysnooper_1

if __name__ == "__main__":
    fuzzer = GrammarFuzzer(grammar_pysnooper_1)
    for i in range(10):
        inp = fuzzer.fuzz()
