from typing import Optional, List, Callable, Set, Union
import random

from isla.derivation_tree import DerivationTree
from debugging_framework.types import Grammar, Expansion, START_SYMBOL

from debugging_framework.fuzzingbook.grammar import (
    is_valid_grammar,
    expansion_to_children,
    nonterminals,
    all_terminals,
)


class Fuzzer:
    """Base class for fuzzers."""

    def __init__(self) -> None:
        pass

    def fuzz(self) -> str:
        """Return fuzz input"""
        return ""

    def run(self):
        """Return fuzz"""
        return self.fuzz()


class GrammarFuzzer(Fuzzer):
    """Produce strings from grammars efficiently, using derivation trees."""

    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str = START_SYMBOL,
        min_nonterminals: int = 0,
        max_nonterminals: int = 10,
        disp: bool = False,
        log: Union[bool, int] = False,
    ) -> None:
        """Produce strings from `grammar`, starting with `start_symbol`.
        If `min_nonterminals` or `max_nonterminals` is given, use them as limits
        for the number of nonterminals produced.
        If `disp` is set, display the intermediate derivation trees.
        If `log` is set, show intermediate steps as text on standard output."""

        self.grammar = grammar
        self.start_symbol = start_symbol
        self.min_nonterminals = min_nonterminals
        self.max_nonterminals = max_nonterminals
        self.disp = disp
        self.log = log
        self.check_grammar()  # Invokes is_valid_grammar()

    def check_grammar(self) -> None:
        """Check the grammar passed"""
        assert self.start_symbol in self.grammar
        assert is_valid_grammar(
            self.grammar,
            start_symbol=self.start_symbol,
            supported_opts=self.supported_opts(),
        )

    def supported_opts(self) -> Set[str]:
        """Set of supported options. To be overloaded in subclasses."""
        return set()  # We don't support specific options

    def init_tree(self) -> DerivationTree:
        return (self.start_symbol, None)

    def choose_node_expansion(
        self, node: DerivationTree, children_alternatives: List[List[DerivationTree]]
    ) -> int:
        """Return index of expansion in `children_alternatives` to be selected.
        'children_alternatives`: a list of possible children for `node`.
        Defaults to random. To be overloaded in subclasses."""
        return random.randrange(0, len(children_alternatives))

    def expansion_to_children(self, expansion: Expansion) -> List[DerivationTree]:
        return expansion_to_children(expansion)

    def expand_node_randomly(self, node: DerivationTree) -> DerivationTree:
        """Choose a random expansion for `node` and return it"""
        (symbol, children) = node
        assert children is None

        if self.log:
            print("Expanding", all_terminals(node), "randomly")

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]
        children_alternatives: List[List[DerivationTree]] = [
            self.expansion_to_children(expansion) for expansion in expansions
        ]

        # ... and select a random expansion
        index = self.choose_node_expansion(node, children_alternatives)
        chosen_children = children_alternatives[index]

        # Process children (for subclasses)
        chosen_children = self.process_chosen_children(
            chosen_children, expansions[index]
        )

        # Return with new children
        return (symbol, chosen_children)

    def process_chosen_children(
        self, chosen_children: List[DerivationTree], expansion: Expansion
    ) -> List[DerivationTree]:
        """Process children after selection.  By default, does nothing."""
        return chosen_children

    def possible_expansions(self, node: DerivationTree) -> int:
        (symbol, children) = node
        if children is None:
            return 1

        return sum(self.possible_expansions(c) for c in children)

    def any_possible_expansions(self, node: DerivationTree) -> bool:
        (symbol, children) = node
        if children is None:
            return True

        return any(self.any_possible_expansions(c) for c in children)

    def choose_tree_expansion(
        self, tree: DerivationTree, children: List[DerivationTree]
    ) -> int:
        """Return index of subtree in `children` to be selected for expansion.
        Defaults to random."""
        return random.randrange(0, len(children))

    def expand_tree_once(self, tree: DerivationTree) -> DerivationTree:
        """Choose an unexpanded symbol in tree; expand it.
        Can be overloaded in subclasses."""
        (symbol, children) = tree
        if children is None:
            # Expand this node
            return self.expand_node(tree)

        # Find all children with possible expansions
        expandable_children = [c for c in children if self.any_possible_expansions(c)]

        # `index_map` translates an index in `expandable_children`
        # back into the original index in `children`
        index_map = [i for (i, c) in enumerate(children) if c in expandable_children]

        # Select a random child
        child_to_be_expanded = self.choose_tree_expansion(tree, expandable_children)

        # Expand in place
        children[index_map[child_to_be_expanded]] = self.expand_tree_once(
            expandable_children[child_to_be_expanded]
        )

        return tree

    def symbol_cost(self, symbol: str, seen: Set[str] = set()) -> Union[int, float]:
        expansions = self.grammar[symbol]
        return min(self.expansion_cost(e, seen | {symbol}) for e in expansions)

    def expansion_cost(
        self, expansion: Expansion, seen: Set[str] = set()
    ) -> Union[int, float]:
        symbols = nonterminals(expansion)
        if len(symbols) == 0:
            return 1  # no symbol

        if any(s in seen for s in symbols):
            return float("inf")

        # the value of a expansion is the sum of all expandable variables
        # inside + 1
        return sum(self.symbol_cost(s, seen) for s in symbols) + 1

    def expand_node_by_cost(
        self, node: DerivationTree, choose: Callable = min
    ) -> DerivationTree:
        (symbol, children) = node
        assert children is None

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]

        children_alternatives_with_cost = [
            (
                self.expansion_to_children(expansion),
                self.expansion_cost(expansion, {symbol}),
                expansion,
            )
            for expansion in expansions
        ]

        costs = [cost for (child, cost, expansion) in children_alternatives_with_cost]
        chosen_cost = choose(costs)
        children_with_chosen_cost = [
            child
            for (child, child_cost, _) in children_alternatives_with_cost
            if child_cost == chosen_cost
        ]
        expansion_with_chosen_cost = [
            expansion
            for (_, child_cost, expansion) in children_alternatives_with_cost
            if child_cost == chosen_cost
        ]

        index = self.choose_node_expansion(node, children_with_chosen_cost)

        chosen_children = children_with_chosen_cost[index]
        chosen_expansion = expansion_with_chosen_cost[index]
        chosen_children = self.process_chosen_children(
            chosen_children, chosen_expansion
        )

        # Return with a new list
        return (symbol, chosen_children)

    def expand_node_min_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at minimum cost")

        return self.expand_node_by_cost(node, min)

    def expand_node_max_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at maximum cost")

        return self.expand_node_by_cost(node, max)

    def log_tree(self, tree: DerivationTree) -> None:
        """Output a tree if self.log is set"""
        if self.log:
            print("Tree:", all_terminals(tree))
            # print(self.possible_expansions(tree), "possible expansion(s) left")

    def expand_tree_with_strategy(
        self,
        tree: DerivationTree,
        expand_node_method: Callable,
        limit: Optional[int] = None,
    ):
        """Expand tree using `expand_node_method` as node expansion function
        until the number of possible expansions reaches `limit`."""
        self.expand_node = expand_node_method  # type: ignore
        while (
            limit is None or self.possible_expansions(tree) < limit
        ) and self.any_possible_expansions(tree):
            tree = self.expand_tree_once(tree)
            self.log_tree(tree)
        return tree

    def expand_tree(self, tree: DerivationTree) -> DerivationTree:
        """Expand `tree` in a three-phase strategy until all expansions are complete."""
        self.log_tree(tree)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_max_cost, self.min_nonterminals
        )
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_randomly, self.max_nonterminals
        )
        tree = self.expand_tree_with_strategy(tree, self.expand_node_min_cost)

        assert self.possible_expansions(tree) == 0

        return tree

    def fuzz_tree(self) -> DerivationTree:
        """Produce a derivation tree from the grammar."""
        tree = self.init_tree()
        # print(tree)

        # Expand all nonterminals
        tree = self.expand_tree(tree)
        if self.log:
            print(repr(all_terminals(tree)))

        return tree

    def fuzz(self) -> str:
        """Produce a string from the grammar."""
        self.derivation_tree = self.fuzz_tree()
        return all_terminals(self.derivation_tree)
