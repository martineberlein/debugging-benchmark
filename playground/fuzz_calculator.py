from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.tools import GrammarBasedEvaluationFuzzer

from debugging_framework.grammar import is_valid_grammar as own
from isla.helpers import is_valid_grammar as isla
from debugging_framework.types import Grammar

grammar_alhazen: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><onenine><maybe_digits><maybe_frac>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": [str(num) for num in range(0, 10)],
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<maybe_frac>": ["", ".<digits>"],
}

def main():
    own(grammar_alhazen)
    isla(grammar_alhazen)


if __name__ == "__main__":
    main()
