import string
import os

from debugging_framework.types import Grammar

two_numbers_grammar: Grammar = {
    "<start>": ["<input>"],
    "<input>": ["<first> <second>"],
    "<first>": ["<integer>"],
    "<second>": ["<integer>"],
    "<integer>": ["<one_nine><maybe_digits>"],
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}

sieve_of_eratosthenes_grammar: Grammar = {
    "<start>": ["<input>"],
    "<input>": ["<integer>"],
    "<integer>": ["<one_nine><maybe_digits>", "0"],
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


__all__ = ["two_numbers_grammar", "sieve_of_eratosthenes_grammar"]
