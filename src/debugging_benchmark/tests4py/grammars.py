import string
import os

from debugging_framework.types import Grammar


grammar_pysnooper: Grammar = {
    "<start>": ["<options>"],
    "<options>": [
        "<output><depth><prefix><watch><custom_repr><overwrite><thread_info>"
    ],
    "<output>": ["-o<ws>", "-o='<path>'<ws>", ""],
    # "<variables>": ["-v<variable_list><ws>", ""],
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
    "<letter>": [letter for letter in string.ascii_letters],
    "<digit>": [digit for digit in string.digits],
    "<char>": ["<letter>", "<digit>", "_"],
    "<int>": ["<nonzero><digits>", "0"],
    "<digits>": ["", "<digits><digit>"],
    "<nonzero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<str>": ["<char><chars>"],
    "<predicate_list>": ["<predicate>", "<predicate_list>,<predicate>"],
    "<predicate>": ["<p_function>=<t_function>"],
    "<p_function>": ["int", "str", "float", "bool"],
    "<t_function>": ["repr", "str", "int"],
    "<ws>": [" "],
}

grammar_youtube_dl_1 = {
    "<start>": ["<match_str>"],
    "<match_str>": ["-q <query> -d <dict>"],
    "<query>": ["<par><stmt_list><par>"],
    "<dict>": ["{<dict_list>}"],
    "<stmt_list>": ["<stmt> & <stmt_list>", "<stmt>"],
    "<stmt>": ["<bool_stmt>", "<comp_stmt>"],
    "<bool_stmt>": ["<unary_op><name>"],
    "<unary_op>": ["!", ""],
    "<comp_stmt>": ["<name> <comp_op><optional> <int>"],
    "<optional>": ["?", ""],
    "<comp_op>": ["<", ">", "<=", ">=", "=", "!="],
    "<dict_list>": ["<kv>, <dict_list>", "<kv>", ""],
    "<kv>": ["<par><name><par>: <value>"],
    "<par>": ["'"],
    "<value>": ["<bool>", "<int>", "'<string>'", "''"],
    "<bool>": ["True", "False", "None"],
    "<name>": [
        "is_live",
        "like_count",
        "description",
        "title",
        "dislike_count",
        "test",
        "other",
    ],
    "<digit>": [str(i) for i in range(10)],
    "<int>": ["<int><digit>", "<digit>"],
    "<string>": ["<string><char>", "<char>"],
    "<char>": [str(char) for char in string.ascii_letters],
}
