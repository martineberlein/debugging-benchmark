import unittest
import string
from debugging_framework.grammar import *


class TestGrammar(unittest.TestCase):
    def setUp(self) -> None:
        calculator_grammar: Grammar = {
            "<start>": ["<arith_expr>"],
            "<arith_expr>": ["<function>(<number>)"],
            "<function>": ["sqrt", "sin", "cos", "tan"],
            "<number>": ["<maybe_minus><one_nine><maybe_digits><maybe_frac>"],
            "<maybe_minus>": ["", "-"],
            "<maybe_frac>": ["", ".<digits>"],
            "<one_nine>": [str(num) for num in range(1, 10)],
            "<digit>": [digit for digit in string.digits],
            "<maybe_digits>": ["", "<digits>"],
            "<digits>": ["<digit>", "<digit><digits>"],
        }

        self.grammar = calculator_grammar

    # TODO: mute stderr
    def test_def_used_nonterminals(self):
        # Das ist nur der Fall, weil die Grammatik so definiert ist
        defined_nonterminals, used_nonterminals = def_used_nonterminals(self.grammar)
        self.assertEqual(defined_nonterminals, used_nonterminals)

        # Test auf defined und used unterschiedlich
        self.grammar.update({"<defined_but_not_used>": ["<digit>"]})
        defined_nonterminals, used_nonterminals = def_used_nonterminals(self.grammar)
        self.assertNotEqual(defined_nonterminals, used_nonterminals)
        self.grammar.pop("<defined_but_not_used>")

        # Test auf eine Expansion keine List in diesem Fall <no_list>
        self.grammar.update({"<no_list>": "just a string"})
        defined_nonterminals, used_nonterminals = def_used_nonterminals(self.grammar)
        self.assertIsNone(defined_nonterminals)
        self.assertIsNone(used_nonterminals)
        self.grammar.pop("<no_list>")

        # Test auf eine Expansion empty List in diesem Fall <empty_list>
        self.grammar.update({"<empty_list>": []})
        defined_nonterminals, used_nonterminals = def_used_nonterminals(self.grammar)
        self.assertIsNone(defined_nonterminals)
        self.assertIsNone(used_nonterminals)
        self.grammar.pop("<empty_list>")

        # Test auf eine Expansion not a string in diesem Fall <not_a_string>
        self.grammar.update({"<not_a_string>": 5})
        defined_nonterminals, used_nonterminals = def_used_nonterminals(self.grammar)
        self.assertIsNone(defined_nonterminals)
        self.assertIsNone(used_nonterminals)
        self.grammar.pop("<not_a_string>")

    def test_nonterminals(self):
        non_terminals = nonterminals("<hello><world>")
        self.assertEqual(non_terminals, ["<hello>", "<world>"])

        non_terminals = nonterminals("<non_terminal>TERMINAL")
        self.assertEqual(non_terminals, ["<non_terminal>"])

    def test_reachable_nonterminals(self):
        reachable = reachable_nonterminals(self.grammar)
        truth = {
            "<start>",
            "<one_nine>",
            "<digit>",
            "<arith_expr>",
            "<function>",
            "<maybe_digits>",
            "<maybe_minus>",
            "<maybe_frac>",
            "<digits>",
            "<number>",
        }
        self.assertEqual(reachable, truth)

        # reachable sollte sich hier nicht verändern
        self.grammar.update({"<not_reachable>": ["<not_reachable>"]})
        reachable = reachable_nonterminals(self.grammar)
        self.assertEqual(reachable, truth)
        self.grammar.pop("<not_reachable>")

    def test_unreachable_nonterminals(self):
        self.grammar.update({"<not_reachable>": ["<not_reachable>"]})
        reachable = unreachable_nonterminals(self.grammar)
        truth = {"<not_reachable>"}
        self.assertEqual(reachable, truth)
        self.grammar.pop("<not_reachable>")

    def test_opts_used(self):
        # weil wir keine options in der grammar haben
        used_opts = opts_used(self.grammar)
        self.assertEqual(used_opts, set())

        self.grammar.update({"<key_with_option>": [("TERMINAL", opts(prob=0.5))]})
        used_opts = opts_used(self.grammar)
        self.assertEqual(used_opts, {"prob"})
        self.grammar.pop("<key_with_option>")

    def test_is_nonterminal(self):
        self.assertTrue(is_nonterminal("<hello>"))
        self.assertFalse(is_nonterminal("TERMINAL"))

    def test_is_valid_grammar(self):
        self.assertTrue(is_valid_grammar(self.grammar))

        self.grammar.update({"<defined_but_not_used>": ["<digit>"]})
        self.grammar.update({"<hello_world>": ["<used_but_not_defined>"]})
        self.grammar.update({"<not_reachable>": ["<not_reachable>"]})
        self.grammar.update({"<key_with_option>": [("TERMINAL", opts(prob=0.5))]})
        self.assertFalse(is_valid_grammar(self.grammar))
        self.grammar.pop("<defined_but_not_used>")
        self.grammar.pop("<hello_world>")
        self.grammar.pop("<not_reachable>")
        self.grammar.pop("<key_with_option>")

    # def test_exp_opts(self):

    # def test_is_valid_probabilistic_grammar(self):


if __name__ == "__main__":
    unittest.main()
