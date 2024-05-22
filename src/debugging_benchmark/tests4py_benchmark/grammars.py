import string
from debugging_framework.types import Grammar

grammar_middle: Grammar = {
    "<start>": ["<x> <y> <z>"],
    "<x>": ["<integer>"],
    "<y>": ["<integer>"],
    "<z>": ["<integer>"],
    "<integer>": ["<integer_>", "-<integer_>"],
    "<integer_>": ["<digit>", "<digit><integer_>"],
    "<digit>": [str(num) for num in range(0, 10)],
}


grammar_expression = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": [
        "<arith_expr><operator><arith_expr>",
        "<number>",
        "(<arith_expr>)",
    ],
    "<operator>": [" + ", " - ", " * ", " / "],
    "<number>": [
        "<maybe_minus><non_zero_digit><maybe_digits>", "0"
    ],
    "<maybe_minus>": ["", "~ "],
    "<non_zero_digit>": [
        str(num) for num in range(1, 10)
    ],  # Exclude 0 from starting digits
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


grammar_markup = {
    "<start>": ["<structure>"],
    "<structure>": ["<string>", "<html><structure>", "<string><html><structure>"],
    "<html>": ["<open><structure><close>"],
    "<open>": ["<LPAR><string><RPAR>"],
    "<close>": ["<LPAR>/<string><RPAR>"],
    "<LPAR>": ["<"],
    "<RPAR>": [">"],
    "<string>": ["", "<str>"],
    "<str>": ["<chars>"],
    "<chars>": ["<char>", "<char><chars>"],
    "<char>": [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "=",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "{",
        "|",
        "}",
        "~",
        " ",
    ],
}

grammar_pysnooper: Grammar = {
    "<start>": ["<options>"],
    "<options>": [" ", "<flag><op>"],
    "<flag>": ["<overwrite><thread_info>"],
    "<op>": [
        "<output><depth><prefix><watch><custom_repr><variables>",
    ],
    "<sep>": [" ", "\n"],
    "<output>": ["-o<sep>", "-o<path><sep>", "-o<sep><path><sep>", ""],
    "<variables>": [
        "-v<variable_list><sep>",
        "-v<sep><variable_list><sep>",
        "-v=<variable_list><sep>",
        "",
    ],
    "<depth>": ["-d<number><sep>", "-d<sep><number><sep>", "-d=<number><sep>", ""],
    "<prefix>": [
        "-p<str_ascii><sep>",
        "-p<sep><str_ascii><sep>",
        "-p=<str_ascii><sep>",
        "",
    ],
    "<watch>": [
        "-w<variable_list><sep>",
        "-w<sep><variable_list><sep>",
        "-w=<variable_list><sep>",
        "",
    ],
    "<custom_repr>": [
        "-c<predicate_list><sep>",
        "-c<sep><predicate_list><sep>",
        "-c=<predicate_list><sep>",
        "",
    ],
    "<overwrite>": ["-O<sep>", ""],
    "<thread_info>": ["-T<sep>", ""],
    "<path>": ["<location>", "<location>.<str_ascii>"],
    "<location>": ["<str_ascii>", "<path>/<str_ascii>"],
    "<variable_list>": ["<variable>", "<variable_list>,<variable>"],
    "<variable>": ["<name>", "<variable>.<name>"],
    "<name>": ["<letter><chars>"],
    "<chars>": ["", "<chars><char>"],
    "<letter>": [letter for letter in string.ascii_letters],
    "<digit>": [digit for digit in string.digits],
    "<char>": [
        "<letter>",
        "<digit>",
        "_",
    ],
    "<predicate_list>": ["<predicate>", "<predicate_list>,<predicate>"],
    "<predicate>": ["<p_function>=<t_function>"],
    "<p_function>": ["int", "str", "float", "bool"],
    "<t_function>": ["repr", "str", "int"],
    "<str_ascii>": ["<chars_ascii>"],
    "<chars_ascii>": ["<char_ascii>", "<char_ascii><chars_ascii>"],
    "<char_ascii>": [str(char) for char in string.ascii_letters + string.digits],
    "<number>": ["<non_zero><digits>"],
    "<non_zero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<digits>": ["", "<digit><digits>"],
}

grammar_pysnooper_1: Grammar = {
    **grammar_pysnooper,
    **{"<op>": ["<output><depth><prefix><watch><custom_repr>"]},
}
grammar_pysnooper_1.pop("<variables>")

grammar_pysnooper_2: Grammar = {
    **grammar_pysnooper,
    **{"<options>": [" ", "<op>"], "<op>": ["<output><depth><prefix><variables>"]},
}
grammar_pysnooper_2.pop("<flag>")
grammar_pysnooper_2.pop("<watch>")
grammar_pysnooper_2.pop("<custom_repr>")
grammar_pysnooper_2.pop("<overwrite>")
grammar_pysnooper_2.pop("<thread_info>")
grammar_pysnooper_2.pop("<predicate_list>")
grammar_pysnooper_2.pop("<t_function>")
grammar_pysnooper_2.pop("<predicate>")
grammar_pysnooper_2.pop("<p_function>")


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


import string

grammar_cookiecutter = {
    "<start>": ["<config>\n<hooks>"],
    "<config>": [
        "{<full_name>,<email>,<github_username>,<project_name>,<repo_name>,<project_short_description>,<release_date>,<year>,<version>}"
    ],
    "<hooks>": ["", "<hook_list>"],
    "<hook_list>": ["<hook>", "<hook_list>\n<hook>"],
    "<hook>": ["<pre_hook>", "<post_hook>"],
    "<pre_hook>": ["pre:<hook_content>"],
    "<post_hook>": ["post:<hook_content>"],
    "<hook_content>": ["echo,<str_with_spaces>", "exit,<int>"],
    "<full_name>": [
        '"full_name":"<str_with_spaces>"',
        '"full_name":[<str_with_spaces_list>]',
    ],
    "<email>": ['"email":"<email_address>"', '"email":[<email_list>]'],
    "<github_username>": [
        '"github_username":"<str>"',
        '"github_username":[<str_list>]',
    ],
    "<project_name>": [
        '"project_name":"<str_with_spaces>"',
        '"project_name":[<str_with_spaces_list>]',
    ],
    "<repo_name>": ['"repo_name":"<str>"', '"repo_name":[<str_list>]'],
    "<project_short_description>": [
        '"project_short_description":"<str_with_spaces>"',
        '"project_short_description":[<str_with_spaces_list>]',
    ],
    "<release_date>": ['"release_date":"<date>"', '"release_date":[<date_list>]'],
    "<year>": ['"year":"<int>"', '"year":[<int_list>]'],
    "<version>": ['"version":"<v>"', '"version":[<version_list>]'],
    "<str_with_spaces_list>": [
        '"<str_with_spaces>"',
        '<str_with_spaces_list>,"<str_with_spaces>"',
    ],
    "<email_list>": ['"<email_address>"', '<email_list>,"<email_address>"'],
    "<str_list>": ['"<str>"', '<str_list>,"<str>"'],
    "<int_list>": ['"<int>"', '<int_list>,"<int>"'],
    "<date_list>": ['"<date>"', '<date_list>,"<date>"'],
    "<version_list>": ['"<v>"', '<version_list>,"<v>"'],
    "<chars>": ["", "<chars><char>"],
    "<char>": [char for char in string.ascii_letters + string.digits + "_"],
    "<chars_with_spaces>": ["", "<chars_with_spaces><char_with_spaces>"],
    "<char_with_spaces>": [
        char for char in string.ascii_letters + string.digits + "_ "
    ],
    "<str>": ["<char><chars>"],
    "<str_with_spaces>": ["<char_with_spaces><chars_with_spaces>"],
    "<email_address>": ["<str>@<str>.<str>"],
    "<date>": ["<day>.<month>.<int>", "<int>-<month>-<day>"],
    "<month>": ["0<nonzero>", "<nonzero>", "10", "11", "12"],
    "<day>": [
        "0<nonzero>",
        "<nonzero>",
        "10",
        "1<nonzero>",
        "20",
        "2<nonzero>",
        "30",
        "31",
    ],
    "<v>": ["<digit><digits>", "<v>.<digit><digits>"],
    "<int>": ["<nonzero><digits>", "0"],
    "<digits>": ["", "<digits><digit>"],
    "<nonzero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<digit>": [char for char in string.digits],
}


if __name__ == "__main__":
    from debugging_framework.fuzzingbook.grammar import is_valid_grammar

    assert is_valid_grammar(grammar_pysnooper_1)
    assert is_valid_grammar(grammar_pysnooper_2)
    assert is_valid_grammar(grammar_cookiecutter)
