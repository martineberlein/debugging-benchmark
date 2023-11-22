from abc import ABC, abstractmethod
from typing import Callable, List

from fuzzingbook.Grammars import Grammar
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)
from fuzzingbook.Parser import EarleyParser
from isla.fuzzer import GrammarFuzzer as ISLaGrammarFuzzer

from debugging_framework.execution_handler import SingleExecutionHandler
from debugging_framework.report import MultipleFailureReport, Report


class Tool(ABC):
    name: str

    def __init__(self, grammar: Grammar, oracle: Callable, initial_inputs: List):
        self.oracle = oracle
        self.grammar = grammar
        self.initial_inputs = initial_inputs
        self.generated_inputs = set()

    @abstractmethod
    def run(self) -> Report:
        raise NotImplementedError

    def get_generated_inputs(self):
        return self.generated_inputs


class GrammarBasedEvaluationTool(Tool, ABC):
    def __init__(
        self,
        grammar,
        oracle,
        initial_inputs,
        max_non_terminals: int = 5,
        max_generated_inputs: int = 10000,
        **kwargs
    ):
        super().__init__(grammar, oracle, initial_inputs)
        self.report = MultipleFailureReport(name=type(self).__name__)
        self.execution_handler = SingleExecutionHandler(self.oracle)

        self.max_non_terminals = max_non_terminals
        self.max_generated_inputs = max_generated_inputs


class GrammarBasedEvaluationFuzzer(GrammarBasedEvaluationTool):
    name = "GrammarBasedFuzzer"

    def run(self) -> Report:
        fuzzer = GrammarFuzzer(self.grammar, max_nonterminals=self.max_non_terminals)

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        self.generated_inputs = test_inputs
        return self.report


class InputsFromHellEvaluationFuzzer(GrammarBasedEvaluationTool):
    name = "InputsFromHellFuzzer"

    def run(self) -> Report:
        prob_grammar = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        ).mine_probabilistic_grammar(inputs=self.initial_inputs)
        fuzzer = ProbabilisticGrammarFuzzer(
            prob_grammar, max_nonterminals=self.max_non_terminals
        )

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        self.generated_inputs = test_inputs
        return self.report


class ISLaGrammarEvaluationFuzzer(GrammarBasedEvaluationTool):
    name = "ISLaGrammarBasedFuzzer"

    def run(self) -> Report:
        fuzzer = ISLaGrammarFuzzer(
            self.grammar, max_nonterminals=self.max_non_terminals
        )

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        self.generated_inputs = test_inputs
        return self.report
