import string
import os

from fuzzingbook.Grammars import srange, Grammar


grammar_pysnooper: Grammar = {
    "<start>": ["<options>"],
    "<options>": [
        "<output><depth><prefix><watch><custom_repr><overwrite><thread_info>"
    ],
    "<output>": ["-o<ws>", "-o='<path>'<ws>", ""],
    #"<variables>": ["-v<variable_list><ws>", ""],
    "<depth>": ["-d=<int><ws>", ""],
    "<prefix>": ["-p='<str>'<ws>", ""],
    "<watch>": ["-w='<variable_list>'<ws>", ""],
    "<custom_repr>": ["-c=<predicate_list><ws>", ""],
    "<overwrite>": ["-O<ws>", ""],
    "<thread_info>": ["-T<ws>", ""],
    "<path>": ["<location>", "<location>.<str>"],
    "<location>": ["<str>", os.path.join("<path>", "<str>")],
    "<variable_list>": ["<variable>", "<variable_list>,<variable>"],
    "<variable>": ["<name>", "<variable>.<name>"],
    "<name>": ["<letter><chars>"],
    "<chars>": ["", "<chars><char>"],
    "<letter>": srange(string.ascii_letters),
    "<digit>": srange(string.digits),
    "<char>": ["<letter>", "<digit>", "_"],
    "<int>": ["<nonzero><digits>", "0"],
    "<digits>": ["", "<digits><digit>"],
    "<nonzero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<str>": ["<char><chars>"],
    "<predicate_list>": ["<predicate>", "<predicate_list>,<predicate>"],
    "<predicate>": ["<p_function>=<t_function>"],
    "<p_function>": ["int", "str", "float", "bool"],
    "<t_function>": ["repr", "str", "int"],
    "<ws>": [" "]
}
