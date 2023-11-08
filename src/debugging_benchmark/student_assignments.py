from typing import Type, List, Callable, Dict
from pathlib import Path
from abc import ABC
import os
import string

from fuzzingbook.Grammars import Grammar

from debugging_framework.oracle import OracleResult
from debugging_framework.oracle_construction import construct_oracle
from debugging_framework.subjects import TestSubject, TestSubjectFactory, load_function_from_class


class MPITestSubject(TestSubject, ABC):
    name: str
    base_path: str
    implementation_class_name: str = "Solution"
    implementation_function_name: str

    def __init__(self, oracle, bug_id):
        super().__init__(oracle=oracle)
        self.id = bug_id

    @classmethod
    def get_dir(cls) -> Path:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        return Path(repo_dir) / Path(cls.base_path)

    @classmethod
    def harness_function(cls, input_str: str):
        param = list(map(int, str(input_str).strip().split()))
        return param

    @classmethod
    def ground_truth(cls) -> Callable:
        solution_file_path = cls.get_dir() / Path("reference1.py")
        return load_function_from_class(
            solution_file_path,
            cls.implementation_class_name,
            cls.implementation_function_name,
        )

    def get_implementation(self) -> Callable:
        imp_file_path = self.get_dir() / Path(f"prog_{self.id}/buggy.py")

        return load_function_from_class(
            imp_file_path,
            self.implementation_class_name,
            self.implementation_function_name,
        )


class GCDTestSubject(MPITestSubject):
    name = "GCD"
    base_path = Path("./student_assignments/problem_1_GCD")
    implementation_function_name = "gcd"
    default_grammar: Grammar = {
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
    default_test_inputs = ["10 2", "4 4"]


class SieveOfEratosthenesTestSubject(MPITestSubject):
    name = "Sieve-of-Eratosthenes"
    base_path = Path("./student_assignments/problem_2_Sieve-of-Eratosthenes")
    implementation_function_name = "sieveOfEratosthenes"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["10", "35"]


class NPrTestSubject(MPITestSubject):
    name = "nPr"
    base_path = Path("./student_assignments/problem_3_nPr")
    implementation_function_name = "nPr"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<first> <second>"],
        "<first>": ["<integer>"],
        "<second>": ["<one_to_twenty>"],
        "<one_to_twenty>": ["<one_nine>", "1<one_nine>", "20"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["2 1", "3 3"]


class FibonacciTestSubject(MPITestSubject):
    name = "Fibonacci"
    base_path = Path("./student_assignments/problem_4_Fibonacci_to_N")
    implementation_function_name = "nFibonacci"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["1", "5"]


class NumberOfDivisorsTestSubject(MPITestSubject):
    name = "Number-of-Divisors"
    base_path = Path("./student_assignments/problem_5_Number-of-divisors")
    implementation_function_name = "count_divisors"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["6", "10"]


class BubbleSortTestSubject(MPITestSubject):
    name = "BubbleSort"
    base_path = Path("./student_assignments/problem_6_Bubble-Sort")
    implementation_function_name = "bubbleSort"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        #TODO: mit mehr integer fürs array beginnen?
        "<input>": ["<integer>\n<integer><maybe_integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<maybe_integer>": ["", " <integer><maybe_integer>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    @classmethod
    def harness_function(cls, input_str: str):
        n = int(input_str.splitlines()[0])
        arr = list(map(int, str(input_str.splitlines()[1]).strip().split()))
        return (arr, n)

class MiddleTestSubject(MPITestSubject):
    name = "Middle"
    base_path = Path("./student_assignments/problem_7_Middle-of-Three")
    implementation_function_name = "middle"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<first> <second> <third>"],
        "<first>": ["<integer>"],
        "<second>": ["<integer>"],
        "<third>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["978 518 300", "162 934 200"]



class PalindromeTestSubject(MPITestSubject):
    name = "Palindrome"
    base_path = Path("./student_assignments/problem_8_Palindrome-String")
    implementation_function_name = "isPalindrome"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<valid>", "<invalid>"],
        "<valid>": ["a<valid>a", "b<valid>b", "c<valid>c", "<character>", ""],
        "<character>": list(string.ascii_lowercase),
        "<invalid>": ["<character><maybe_character>"],
        "<maybe_character>": ["<character><maybe_character>", ""]
    }
    default_test_inputs = ["abba", "abc"]

    #eigentlich nicht nötig, aber per default wird ja was gemacht
    #in oracle wird gecheckt ob es eine harness function gibt aber per default gibt es eine oder? line 60
    @classmethod
    def harness_function(cls, input_str: str):
        return input_str

class RemoveVowelTestSubject(MPITestSubject):
    name = "Remove Vowel"
    base_path = Path("./student_assignments/problem_9_Remove-vowels-from-string")
    implementation_function_name = "removeVowels"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<word><maybe_word>"],
        "<maybe_word>": [" <word><maybe_word>", ""],
        "<word>": ["<char><maybe_char>"],        
        "<char>": list(string.ascii_lowercase),
        "<maybe_char>": ["<char><maybe_char>", ""]     
    }
    default_test_inputs = ["welcome to avicenna", "hello my name is martin"]

    #eigentlich nicht nötig, aber per default wird ja was gemacht
    #in oracle wird gecheckt ob es eine harness function gibt aber per default gibt es eine oder? line 60
    @classmethod
    def harness_function(cls, input_str: str):
        return input_str

class SquareRootTestSubject(MPITestSubject):
    name = "SquareRoot"
    base_path = Path("./student_assignments/problem_10_Square-root")
    implementation_function_name = "floorSqrt"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["4", "5"]

class MergeStringsTestSubject(MPITestSubject):
    name = "Merge Strings"
    base_path = Path("./student_assignments/problem_11_Merge-two-strings")
    implementation_function_name = "merge"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<word> <word>"],
        "<word>": ["<character><maybe_character>"],        
        "<character>": list(string.ascii_lowercase),
        "<maybe_character>": ["<character><maybe_character>", ""],        
    }
    default_test_inputs = ["abc def", "hello bye"]

    @classmethod
    def harness_function(cls, input_str: str):
        S1, S2 = map(str, str(input_str).strip().split())
        return (S1, S2)
  
class MPITestSubjectFactory(TestSubjectFactory):
    def __init__(self, test_subject_types: List[Type[MPITestSubject]]):
        self.test_subject_types = test_subject_types

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[MPITestSubject]:
        subjects = []

        for subject_type in self.test_subject_types:
            for subject_id in range(1, 11):
                try:
                    subject = self._build_subject(
                        subject_type, subject_id, err_def, default_oracle
                    )
                    subjects.append(subject)
                except Exception as e:
                    print(f"Subject {subject_id} could not be built.")
                    print(e)

        return subjects

    @staticmethod
    def _build_subject(
        subject_type,
        subject_id,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> MPITestSubject:
        subject_path = subject_type.get_dir() / Path(f"prog_{subject_id}/buggy.py")

        reference = subject_type.ground_truth()

        loaded_function = load_function_from_class(
            subject_path,
            subject_type.implementation_class_name,
            subject_type.implementation_function_name,
        )

        error_def = err_def or {TimeoutError: OracleResult.UNDEFINED}
        def_oracle = default_oracle or OracleResult.FAILING

        oracle = construct_oracle(
            loaded_function,
            reference,
            error_def,
            default_oracle_result=def_oracle,
            timeout=0.01,
            harness_function=subject_type.harness_function,
        )
        subject = subject_type(oracle=oracle, bug_id=subject_id)
        return subject


def main():
    subject_type = NumberOfDivisorsTestSubject
    subjects = MPITestSubjectFactory([subject_type]).build()

    def_inputs = subject_type.default_test_inputs
    print("Ground Truth")
    for inp in def_inputs:
        param = subject_type.harness_function(inp)
        print(subject_type.ground_truth()(*param))

    for subject in subjects:
        print(f"Subject {subject.id}")
        param = subject.to_dict()
        oracle = param.get("oracle")
        for inp in param.get("initial_inputs"):
            print(inp, oracle(inp))


if __name__ == "__main__":
    main()
