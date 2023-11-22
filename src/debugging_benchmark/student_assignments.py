from typing import  List, Dict, Sequence, Any, Callable
from pathlib import Path
from abc import ABC, abstractmethod
import os
import string

from fuzzingbook.Grammars import Grammar

from debugging_framework.oracle import OracleResult
from debugging_framework.oracle_construction import construct_oracle
from debugging_framework.benchmark import load_function_from_class

from debugging_framework.benchmark import BenchmarkRepository, BenchmarkProgram


class StudentAssignmentBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        initial_inputs: List[str],
        oracle: Callable,
    ):
        super().__init__(name, grammar, oracle, initial_inputs)
        self.bug_id = bug_id

    def __repr__(self):
        return f"{self.name}_{self.bug_id}"

    def get_name(self) -> str:
        return self.__repr__()

    def get_grammar(self):
        return self.grammar

    def get_initial_inputs(self):
        return self.initial_inputs

    def get_oracle(self):
        return self.oracle


class StudentAssignmentRepository(BenchmarkRepository, ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError(
            "A StudentAssignment-Benchmark-Repository needs to have a unique name."
        )
    
    def get_dir(self) -> Path:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(Path(repo_dir),Path("student_assignments"))

    def get_ground_truth_location(self):
        return os.path.join(self.get_dir(), Path("reference1.py"))
    
    def load_ground_truth(self):
        path_to_ground_truth = self.get_ground_truth_location()
        return load_function_from_class(
            path_to_ground_truth,
            self.get_implementation_function_name()
        )
    
    def load_implementation(self, bug_id) -> Callable:
        path_to_implementation = os.path.join(self.get_dir(),Path(f"prog_{bug_id}/buggy.py"))

        return load_function_from_class(
            path_to_implementation,
            self.get_implementation_function_name()
        )
    
    def _construct_test_program(
        self,
        bug_id,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None
    ) -> StudentAssignmentBenchmarkProgram:
        ground_truth = self.load_ground_truth()
        program = self.load_implementation(bug_id)
        
        oracle = construct_oracle(
            program,
            ground_truth,
            err_def,
            default_oracle_result=default_oracle,
            timeout=0.01,
            harness_function=self.harness_function
        )

        return StudentAssignmentBenchmarkProgram(
            name=self.get_name(),
            bug_id=bug_id,
            grammar=self.get_grammar(),
            initial_inputs=self.get_initial_inputs(),
            oracle=oracle,
        )
    
    def build(
            self,
            err_def: Dict[Exception, OracleResult] = None,
            default_oracle: OracleResult = None,
    ) -> List[StudentAssignmentBenchmarkProgram]:
        
        constructed_test_programs: List[StudentAssignmentBenchmarkProgram] = []
        
        for bug_id in range(1,11):
            try:
                subject = self._construct_test_program(
                    bug_id,
                    err_def,
                    default_oracle
                )
                
                constructed_test_programs.append(subject)
            except Exception as e:
                    print(f"Subject {bug_id} could not be built.")
                    print(e)            
                
        return constructed_test_programs    
    
    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass
    

class GCDStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "GCD"
        self._implementation_function_name: str = "gcd"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_1_GCD"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
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

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["10 2", "4 4"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param

class SieveOfEratosthenesStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Sieve-of-Eratosthenes"
        self._implementation_function_name: str = "sieveOfEratosthenes"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_2_Sieve-of-Eratosthenes"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["10", "35"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param

class NPrStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "nPr"
        self._implementation_function_name: str = "nPr"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_3_nPr"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
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

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["2 1", "3 3"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param
    
class FibonacciStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Fibonacci"
        self._implementation_function_name: str = "nFibonacci"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_4_Fibonacci_to_N"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["1", "5"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param
    
class NumberOfDivisorsAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Number-of-Divisors"
        self._implementation_function_name: str = "count_divisors"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_5_Number-of-divisors"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["6", "10"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param
    
class BubbleSortAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "BubbleSort"
        self._implementation_function_name: str = "bubbleSort"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_6_Bubble-Sort"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<integer>\n<integer><maybe_integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<maybe_integer>": ["", " <integer><maybe_integer>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        n = int(input_str.splitlines()[0])
        arr = list(map(int, str(input_str.splitlines()[1]).strip().split()))
        return (arr, n)
    
class MiddleAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Middle"
        self._implementation_function_name: str = "middle"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_7_Middle-of-Three"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
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

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["978 518 300", "162 934 200"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param
    
class PalindromeAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Palindrome"
        self._implementation_function_name: str = "isPalindrome"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_8_Palindrome-String"))

    #TODO: restliche Regeln implementiern, gibts eine smartere Lsg?
    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<valid>", "<invalid>"],
        "<valid>": ["a<valid>a", "b<valid>b", "c<valid>c", "<character>", ""],
        "<character>": list(string.ascii_lowercase),
        "<invalid>": ["<character><maybe_character>"],
        "<maybe_character>": ["<character><maybe_character>", ""]
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["abba", "abc"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return input_str
    
class RemoveVowelAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Remove Vowel"
        self._implementation_function_name: str = "removeVowels"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_9_Remove-vowels-from-string"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<word><maybe_word>"],
        "<maybe_word>": [" <word><maybe_word>", ""],
        "<word>": ["<char><maybe_char>"],        
        "<char>": list(string.ascii_lowercase),
        "<maybe_char>": ["<char><maybe_char>", ""]     
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["welcome to avicenna", "hello my name is martin"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return input_str
    
class SquareRootAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "SquareRoot"
        self._implementation_function_name: str = "floorSqrt"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_10_Square-root"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["4", "5"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param

class MergeStringsAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Merge Strings"
        self._implementation_function_name: str = "merge"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name
        
    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_11_Merge-two-strings"))

    @staticmethod
    def get_grammar() -> Grammar:
        return {
        "<start>": ["<input>"],
        "<input>": ["<word> <word>"],
        "<word>": ["<character><maybe_character>"],        
        "<character>": list(string.ascii_lowercase),
        "<maybe_character>": ["<character><maybe_character>", ""],        
    }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["abc def", "hello bye"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        S1, S2 = map(str, str(input_str).strip().split())
        return (S1, S2)
