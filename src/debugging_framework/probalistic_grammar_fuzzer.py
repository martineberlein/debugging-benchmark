import random
from typing import List

from debugging_framework.types import DerivationTree
from debugging_framework.grammar import exp_probabilities, all_terminals
from debugging_framework.grammar_fuzzer import GrammarFuzzer

class ProbabilisticGrammarFuzzer(GrammarFuzzer):

    def choose_node_expansion(self,
                              node: DerivationTree,
                              children_alternatives: List[List[DerivationTree]]) -> int:
        (symbol, tree) = node
        expansions = self.grammar[symbol]
        probabilities = exp_probabilities(expansions)

        weights: List[float] = []
        for children in children_alternatives:
            expansion = all_terminals((symbol, children))
            children_weight = probabilities[expansion]
            if self.log:
                print(repr(expansion), "p =", children_weight)
            weights.append(children_weight)

        if sum(weights) == 0:
            # No alternative (probably expanding at minimum cost)
            return random.choices(
                range(len(children_alternatives)))[0]
        else:
            return random.choices(
                range(len(children_alternatives)), weights=weights)[0]