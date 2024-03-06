import sys
import re
import copy
from typing import Set, Optional, Tuple, Dict, Any, cast, Union, List

from isla.derivation_tree import DerivationTree
from debugging_framework.types import (
    Grammar,
    Expansion,
    START_SYMBOL,
    RE_NONTERMINAL,
    Option,
)


def is_valid_grammar(
    grammar: Grammar, start_symbol: str = START_SYMBOL, supported_opts: Set[str] = set()
) -> bool:
    """Check if the given `grammar` is valid.
    `start_symbol`: optional start symbol (default: `<start>`)
    `supported_opts`: options supported (default: none)"""

    defined_nonterminals, used_nonterminals = def_used_nonterminals(
        grammar, start_symbol
    )
    if defined_nonterminals is None or used_nonterminals is None:
        return False

    # Do not complain about '<start>' being not used,
    # even if start_symbol is different
    # TODO: eigentlich überflüssig, da das schon in def_used_nonterminals passiert
    if START_SYMBOL in grammar:
        used_nonterminals.add(START_SYMBOL)

    for unused_nonterminal in defined_nonterminals - used_nonterminals:
        print(repr(unused_nonterminal) + ": defined, but not used", file=sys.stderr)
    for undefined_nonterminal in used_nonterminals - defined_nonterminals:
        print(repr(undefined_nonterminal) + ": used, but not defined", file=sys.stderr)

    # Symbols must be reachable either from <start> or given start symbol
    unreachable = unreachable_nonterminals(grammar, start_symbol)
    msg_start_symbol = start_symbol

    if START_SYMBOL in grammar:
        unreachable = unreachable - reachable_nonterminals(grammar, START_SYMBOL)
        if start_symbol != START_SYMBOL:
            msg_start_symbol += " or " + START_SYMBOL

    for unreachable_nonterminal in unreachable:
        print(
            repr(unreachable_nonterminal) + ": unreachable from " + msg_start_symbol,
            file=sys.stderr,
        )

    used_but_not_supported_opts = set()
    if len(supported_opts) > 0:
        used_but_not_supported_opts = opts_used(grammar).difference(supported_opts)
        for opt in used_but_not_supported_opts:
            print("warning: option " + repr(opt) + " is not supported", file=sys.stderr)

    return used_nonterminals == defined_nonterminals and len(unreachable) == 0


def def_used_nonterminals(
    grammar: Grammar, start_symbol: str = START_SYMBOL
) -> Tuple[Optional[Set[str]], Optional[Set[str]]]:
    """Return a pair (`defined_nonterminals`, `used_nonterminals`) in `grammar`.
    In case of error, return (`None`, `None`)."""

    defined_nonterminals = set()
    used_nonterminals = {start_symbol}

    for defined_nonterminal in grammar:
        defined_nonterminals.add(defined_nonterminal)
        expansions = grammar[defined_nonterminal]
        if not isinstance(expansions, list):
            print(
                repr(defined_nonterminal) + ": expansion is not a list", file=sys.stderr
            )
            return None, None

        if len(expansions) == 0:
            print(repr(defined_nonterminal) + ": expansion list empty", file=sys.stderr)
            return None, None

        for expansion in expansions:
            if isinstance(expansion, tuple):
                expansion = expansion[0]
            if not isinstance(expansion, str):
                print(
                    repr(defined_nonterminal)
                    + ": "
                    + repr(expansion)
                    + ": not a string",
                    file=sys.stderr,
                )
                return None, None

            for used_nonterminal in nonterminals(expansion):
                used_nonterminals.add(used_nonterminal)

    return defined_nonterminals, used_nonterminals


def reachable_nonterminals(
    grammar: Grammar, start_symbol: str = START_SYMBOL
) -> Set[str]:
    reachable = set()

    def _find_reachable_nonterminals(grammar, symbol):
        nonlocal reachable
        reachable.add(symbol)
        for expansion in grammar.get(symbol, []):
            for nonterminal in nonterminals(expansion):
                if nonterminal not in reachable:
                    _find_reachable_nonterminals(grammar, nonterminal)

    _find_reachable_nonterminals(grammar, start_symbol)
    return reachable


def unreachable_nonterminals(grammar: Grammar, start_symbol=START_SYMBOL) -> Set[str]:
    return grammar.keys() - reachable_nonterminals(grammar, start_symbol)


def nonterminals(expansion: str):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return RE_NONTERMINAL.findall(expansion)


def is_nonterminal(s):
    return RE_NONTERMINAL.match(s)


def opts_used(grammar: Grammar) -> Set[str]:
    used_opts = set()
    for symbol in grammar:
        for expansion in grammar[symbol]:
            # |= in place or
            # https://stackoverflow.com/questions/3929278/what-does-ior-do-in-python
            used_opts |= set(exp_opts(expansion).keys())
    return used_opts


def exp_opts(expansion: Expansion) -> Dict[str, Any]:
    """Return the options of an expansion.  If options are not defined, return {}"""
    if isinstance(expansion, str):
        return {}
    return expansion[1]


def is_valid_probabilistic_grammar(
    grammar: Grammar, start_symbol: str = START_SYMBOL
) -> bool:
    if not is_valid_grammar(grammar, start_symbol):
        return False

    for nonterminal in grammar:
        expansions = grammar[nonterminal]
        _ = exp_probabilities(expansions, nonterminal)

    return True


def exp_probabilities(
    expansions: List[Expansion], nonterminal: str = "<symbol>"
) -> Dict[Expansion, float]:
    probabilities = [exp_prob(expansion) for expansion in expansions]
    prob_dist = prob_distribution(probabilities, nonterminal)  # type: ignore

    prob_mapping: Dict[Expansion, float] = {}
    for i in range(len(expansions)):
        expansion = exp_string(expansions[i])
        prob_mapping[expansion] = prob_dist[i]

    return prob_mapping


def all_terminals(tree: DerivationTree) -> str:
    (symbol, children) = tree
    if children is None:
        # This is a nonterminal symbol not expanded yet
        return symbol

    if len(children) == 0:
        # This is a terminal symbol
        return symbol

    # This is an expanded symbol:
    # Concatenate all terminal symbols from all children
    return "".join([all_terminals(c) for c in children])


def extend_grammar(grammar: Grammar, extension: Grammar = {}) -> Grammar:
    new_grammar = copy.deepcopy(grammar)
    new_grammar.update(extension)
    return new_grammar


def expansion_key(
    symbol: str,
    expansion: Union[Expansion, Tuple[str, Optional[List[Any]]], List[DerivationTree]],
) -> str:
    """Convert (symbol, `expansion`) into a key "SYMBOL -> EXPRESSION".
    `expansion` can be an expansion string, a derivation tree,
       or a list of derivation trees."""

    if isinstance(expansion, tuple):
        # Expansion or single derivation tree
        expansion, _ = expansion

    # Check for empty list expansion
    if isinstance(expansion, list) and not expansion:
        expansion = ""

    if not isinstance(expansion, str):
        # Derivation tree
        children = expansion
        expansion = all_terminals((symbol, children))

    assert isinstance(expansion, str)

    return symbol + " -> " + expansion


def set_prob(
    grammar: Grammar, symbol: str, expansion: Expansion, prob: Optional[float]
) -> None:
    """Set the probability of the given expansion of grammar[symbol]"""
    set_opts(grammar, symbol, expansion, opts(prob=prob))


def set_opts(
    grammar: Grammar, symbol: str, expansion: Expansion, opts: Option = {}
) -> None:
    """Set the options of the given expansion of grammar[symbol] to opts"""
    expansions = grammar[symbol]
    for i, exp in enumerate(expansions):
        if exp_string(exp) != exp_string(expansion):
            continue

        new_opts = exp_opts(exp)
        if opts == {} or new_opts == {}:
            new_opts = opts
        else:
            for key in opts:
                new_opts[key] = opts[key]

        if new_opts == {}:
            grammar[symbol][i] = exp_string(exp)
        else:
            grammar[symbol][i] = (exp_string(exp), new_opts)

        return


def opts(**kwargs: Any) -> Dict[str, Any]:
    return kwargs


def exp_prob(expansion: Expansion) -> float:
    """Return the options of an expansion"""
    return exp_opt(expansion, "prob")


def exp_opt(expansion: Expansion, attribute: str) -> Any:
    """Return the given attribution of an expansion.
    If attribute is not defined, return None"""
    return exp_opts(expansion).get(attribute, None)


def prob_distribution(
    probabilities: List[Optional[float]], nonterminal: str = "<symbol>"
):
    epsilon = 0.00001

    number_of_unspecified_probabilities = probabilities.count(None)
    if number_of_unspecified_probabilities == 0:
        sum_probabilities = cast(float, sum(probabilities))
        assert abs(sum_probabilities - 1.0) < epsilon, (
            nonterminal + ": sum of probabilities must be 1.0"
        )
        return probabilities

    sum_of_specified_probabilities = 0.0
    for p in probabilities:
        if p is not None:
            sum_of_specified_probabilities += p
    assert 0 <= sum_of_specified_probabilities <= 1.0, (
        nonterminal + ": sum of specified probabilities must be between 0.0 and 1.0"
    )

    default_probability = (
        1.0 - sum_of_specified_probabilities
    ) / number_of_unspecified_probabilities
    all_probabilities = []
    for p in probabilities:
        if p is None:
            p = default_probability
        all_probabilities.append(p)

    assert abs(sum(all_probabilities) - 1.0) < epsilon
    return all_probabilities


def exp_string(expansion: Expansion) -> str:
    """Return the string to be expanded"""
    if isinstance(expansion, str):
        return expansion
    return expansion[0]


def expansion_to_children(expansion: Expansion) -> List[DerivationTree]:
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and nonterminals such
    # that ''.join(strings) == expansion

    expansion = exp_string(expansion)
    assert isinstance(expansion, str)

    if expansion == "":  # Special case: epsilon expansion
        return [("", [])]

    strings = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, []) for s in strings if len(s) > 0]
