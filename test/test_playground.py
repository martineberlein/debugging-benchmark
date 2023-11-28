import unittest
import string

from fuzzingbook.Grammars import is_valid_grammar, Grammar
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.GrammarFuzzer import tree_to_string, display_tree

from debugging_framework.benchmark import get_class_name
from pathlib import Path

class TestInputs(unittest.TestCase):

    @unittest.skip
    def test_harness(self):
        input_str = "5\n4 1 3 9 7"
        n = int(input_str.splitlines()[0])
        arr = list(map(int, str(input_str.splitlines()[1]).strip().split()))
        print(n, arr)
        print(list(string.ascii_lowercase))
        input_str = "hello bye"
        S1, S2 = map(str, str(input_str).strip().split())
        print(S1, S2)

    @unittest.skip
    def test_grammar(self):
        default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<word><maybe_word>"],
        "<maybe_word>": [" <word><maybe_word>", ""],
        "<word>": ["<char><maybe_char>"],        
        "<char>": list(string.ascii_lowercase),
        "<maybe_char>": ["<char><maybe_char>", ""]     
    }
        default_test_inputs = ["w", "hello my name is martin"]

        parser = EarleyParser(default_grammar)
        trees = parser.parse(default_test_inputs[0])
        for tree in trees:
            print(tree)
            
    @unittest.skip
    def test_load(self):
        path = Path("/home/kai/dev/work/debugging-benchmark/src/debugging_benchmark/student_assignments/problem_1_GCD/prog_1/buggy.py")
        class_name = get_class_name(path)
        print(class_name)


if __name__ == "__main__":
    unittest.main()