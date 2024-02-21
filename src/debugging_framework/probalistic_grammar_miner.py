from typing import Dict, List

from isla.parser import Parser
from isla.derivation_tree import DerivationTree

from debugging_framework.types import Grammar
from debugging_framework.grammar import (is_nonterminal,
                                         extend_grammar,
                                         expansion_key,
                                         set_prob)


class ExpansionCountMiner:
    def __init__(self, parser: Parser, log: bool = False) -> None:
        assert isinstance(parser, Parser)
        self.grammar = extend_grammar(parser.grammar())
        self.parser = parser
        self.log = log
        self.reset()

    def reset(self) -> None:
        self.expansion_counts: Dict[str, int] = {}

    def add_coverage(self, symbol: str, children: List[DerivationTree]) -> None:
        key = expansion_key(symbol, children)

        if self.log:
            print("Found", key)

        if key not in self.expansion_counts:
            self.expansion_counts[key] = 0
        self.expansion_counts[key] += 1

    def add_tree(self, tree: DerivationTree) -> None:
        (symbol, children) = tree
        if not is_nonterminal(symbol):
            return
        assert children is not None

        direct_children: List[DerivationTree] = [
            (symbol, None) if is_nonterminal(symbol) 
            else (symbol, []) for symbol, c in children]
        self.add_coverage(symbol, direct_children)

        for c in children:
            self.add_tree(c)

    def count_expansions(self, inputs: List[str]) -> None:
        for inp in inputs:
            tree, *_ = self.parser.parse(inp)
            self.add_tree(tree)

    def counts(self) -> Dict[str, int]:
        return self.expansion_counts
    
class ProbabilisticGrammarMiner(ExpansionCountMiner):
    def __init__(self, parser: Parser, log: bool = False) -> None:
        super().__init__(parser, log)

    def set_probabilities(self, counts: Dict[str, int]):
        for symbol in self.grammar:
            self.set_expansion_probabilities(symbol, counts)

    def set_expansion_probabilities(self, symbol: str, counts: Dict[str, int]):
        expansions = self.grammar[symbol]
        if len(expansions) == 1:
            set_prob(self.grammar, symbol, expansions[0], None)
            return

        expansion_counts = [
            counts.get(
                expansion_key(
                    symbol,
                    expansion),
                0) for expansion in expansions]
        total = sum(expansion_counts)
        for i, expansion in enumerate(expansions):
            p = expansion_counts[i] / total if total > 0 else None
            # if self.log:
            #     print("Setting", expansion_key(symbol, expansion), p)
            set_prob(self.grammar, symbol, expansion, p)
            
    def mine_probabilistic_grammar(self, inputs: List[str]) -> Grammar:
        self.count_expansions(inputs)
        self.set_probabilities(self.counts())
        return self.grammar