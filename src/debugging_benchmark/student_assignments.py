from typing import List, Dict, Sequence, Any, Callable, Type
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import string

from debugging_framework.types import Grammar
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
        self.passing_input = []
        self.failing_input = []

    def __repr__(self):
        return f"{self.name}_{self.bug_id}"

    def get_name(self) -> str:
        return self.__repr__()

    def get_grammar(self) -> Grammar:
        return self.grammar

    def get_initial_inputs(self) -> List[str]:
        return self.passing_input + self.failing_input

    def get_passing_inputs(self) -> List[str]:
        return self.passing_input

    def get_failing_input(self) -> List[str]:
        return self.failing_input

    def get_oracle(self) -> Callable:
        return self.oracle


class StudentAssignmentRepository(BenchmarkRepository, ABC):
    programs: List[Type[StudentAssignmentBenchmarkProgram]]

    @abstractmethod
    def get_implementation_function_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError(
            "A StudentAssignment-Benchmark-Repository needs to have a unique name."
        )

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        raise NotImplementedError

    def get_dir(self) -> Path:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(Path(repo_dir), Path("student_assignments"))

    def get_ground_truth_location(self) -> Path:
        return os.path.join(self.get_dir(), Path("reference1.py"))

    def load_ground_truth(self):
        path_to_ground_truth = self.get_ground_truth_location()
        return load_function_from_class(
            path_to_ground_truth, self.get_implementation_function_name()
        )

    def load_implementation(self, bug_id) -> Callable:
        path_to_implementation = os.path.join(
            self.get_dir(), Path(f"prog_{bug_id}/buggy.py")
        )

        return load_function_from_class(
            path_to_implementation, self.get_implementation_function_name()
        )

    def _construct_test_program(
        self,
        bug_id: int,
        benchmark_program: Type[StudentAssignmentBenchmarkProgram],
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> StudentAssignmentBenchmarkProgram:
        ground_truth = self.load_ground_truth()
        program = self.load_implementation(bug_id)

        oracle = construct_oracle(
            program_under_test=program,
            program_oracle=ground_truth,
            error_definitions=err_def,
            default_oracle_result=default_oracle,
            timeout=0.01,
            harness_function=self.harness_function,
        )

        return benchmark_program(
            name=self.get_name(),
            bug_id=bug_id,
            grammar=self.get_grammar(),
            # initial_inputs=self.get_initial_inputs(),
            oracle=oracle,
        )

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[StudentAssignmentBenchmarkProgram]:
        constructed_test_programs: List[StudentAssignmentBenchmarkProgram] = []
        for bug_id, program in enumerate(self.programs):
            try:
                subject = self._construct_test_program(
                    bug_id=bug_id + 1,
                    benchmark_program=program,
                    err_def=err_def,
                    default_oracle=default_oracle,
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
        self.programs: List[Type[StudentAssignmentBenchmarkProgram]] = [
            GCD_1,
            GCD_2,
            GCD_3,
            GCD_4,
            GCD_5,
            GCD_6,
            GCD_7,
            GCD_8,
            GCD_9,
            GCD_10,
        ]

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
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param


@dataclass(repr=False)
class GCD_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar
    oracle: Callable
    failing_input = ["43 38", "10 2", "4 4"]
    passing_input = []


@dataclass(repr=False)
class GCD_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar
    oracle: Callable
    failing_input = ["43 38"]
    passing_input = ["10 2", "4 4"]


@dataclass(repr=False)
class GCD_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar
    oracle: Callable
    failing_input = ["21 21", "4 4"]
    passing_input = ["10 2"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["21 38"]
    passing_input = ["10 2", "4 4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["43 38"]
    passing_input = ["10 2", "4 4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["21 21", "4 4"]
    passing_input = ["10 2"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["43 38", "10 2"]
    passing_input = ["4 4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["194067000 194067"]
    passing_input = ["10 2", "4 4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8 80", "4 4"]
    passing_input = ["10 2"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class GCD_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable

    failing_input = ["8 80", "10 2"]
    passing_input = ["4 4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class SieveOfEratosthenesStudentAssignmentBenchmarkRepository(
    StudentAssignmentRepository
):
    def __init__(self):
        self.name: str = "Sieve-of-Eratosthenes"
        self._implementation_function_name: str = "sieveOfEratosthenes"
        self.programs = [
            sieve_1,
            sieve_2,
            sieve_3,
            sieve_4,
            sieve_5,
            sieve_6,
            sieve_7,
            sieve_8,
            sieve_9,
            sieve_10,
        ]

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
        return ["10"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param


@dataclass(repr=False)
class sieve_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["10000"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7507"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4272", "10"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4272", "10"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4272", "10"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7507"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7", "10"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sieve_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class NPrStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "nPr"
        self._implementation_function_name: str = "nPr"
        self.programs = [
            nPr_1,
            nPr_2,
            nPr_3,
            nPr_4,
            nPr_5,
            nPr_6,
            nPr_7,
            nPr_8,
            nPr_9,
            nPr_10,
        ]

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


@dataclass(repr=False)
class nPr_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8 8", "3 3"]
    passing_input = ["2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4", "3 3"]
    passing_input = ["2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7 6"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4"]
    passing_input = ["2 1", "3 3"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8 8", "3 3"]
    passing_input = ["2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class nPr_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["11 4", "3 3"]
    passing_input = ["2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class FibonacciStudentAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Fibonacci"
        self._implementation_function_name: str = "nFibonacci"
        self.programs = [
            fib_1,
            fib_2,
            fib_3,
            fib_4,
            fib_5,
            fib_6,
            fib_7,
            fib_8,
            fib_9,
            fib_10,
        ]

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


@dataclass(repr=False)
class fib_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["5"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1000000000"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["5"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["5"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["5"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class fib_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["2"]
    passing_input = ["1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class NumberOfDivisorsAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Number-of-Divisors"
        self._implementation_function_name: str = "count_divisors"
        self.programs = [
            div_1,
            div_2,
            div_3,
            div_4,
            div_5,
            div_6,
            div_7,
            div_8,
            div_9,
            div_10,
        ]

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


@dataclass(repr=False)
class div_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1", "6", "10"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["100000"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["30"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["18"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["6"]
    passing_input = ["10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["18"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["7"]
    passing_input = ["6", "10"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1", "10"]
    passing_input = ["6"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class div_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1", "10"]
    passing_input = ["6"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class BubbleSortAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "BubbleSort"
        self._implementation_function_name: str = "bubbleSort"
        self.programs = [
            bubble_1,
            bubble_2,
            bubble_3,
            bubble_4,
            bubble_5,
            bubble_6,
            bubble_7,
            bubble_8,
            bubble_9,
            bubble_10,
        ]

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
    def harness_function(input_str: str) -> Sequence[Any]:
        n = int(input_str.splitlines()[0])
        arr = list(map(int, str(input_str.splitlines()[1]).strip().split()))
        return arr, n


@dataclass(repr=False)
class bubble_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = [
        "8\n24 18 38 43 14 40 1 54",
        "5\n4 1 3 9 7",
        "10\n10 9 8 7 6 5 4 3 2 1",
    ]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["5\n91 23 32 74 6"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["8\n24 18 38 43 14 40 1 54"]
    passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class bubble_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = [
        "8\n24 18 38 43 14 40 1 54",
        "5\n4 1 3 9 7",
        "10\n10 9 8 7 6 5 4 3 2 1",
    ]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class MiddleAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Middle"
        self._implementation_function_name: str = "middle"
        self.programs = [
            middle_1,
            middle_2,
            middle_3,
            middle_4,
            middle_5,
            middle_6,
            middle_7,
            middle_8,
            middle_9,
            middle_10,
        ]

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


@dataclass(repr=False)
class middle_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["124 153 97", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["124 153 97", "978 518 300"]
    passing_input = ["162 934 200"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["312 62 478", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["124 153 97", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["13 39 485", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["124 153 97", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["13 39 485"]
    passing_input = ["978 518 300", "162 934 200"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["124 153 97", "978 518 300", "162 934 200"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["312 62 478", "162 934 200"]
    passing_input = ["978 518 300"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class middle_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["459 8 20"]
    passing_input = ["978 518 300", "162 934 200"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class PalindromeAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Palindrome"
        self._implementation_function_name: str = "isPalindrome"
        self.programs = [
            palindrome_1,
            palindrome_2,
            palindrome_3,
            palindrome_4,
            palindrome_5,
            palindrome_6,
            palindrome_7,
            palindrome_8,
            palindrome_9,
            palindrome_10,
        ]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return os.path.join(super().get_dir(), Path("problem_8_Palindrome-String"))

    # TODO: restliche Regeln implementiern, gibts eine smartere Lsg?
    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<valid>", "<invalid>"],
            "<valid>": [
                "a<valid>a",
                "b<valid>b",
                "c<valid>c",
                "d<valid>d",
                "e<valid>e",
                "f<valid>f",
                "g<valid>g",
                "h<valid>h",
                "i<valid>i",
                "j<valid>j",
                "k<valid>k",
                "l<valid>l",
                "m<valid>m",
                "n<valid>n",
                "o<valid>o",
                "p<valid>p",
                "q<valid>q",
                "r<valid>r",
                "s<valid>s",
                "t<valid>t",
                "u<valid>u",
                "v<valid>v",
                "w<valid>w",
                "x<valid>x",
                "y<valid>y",
                "z<valid>z",
                "<character>",
                "",
            ],
            "<character>": list(string.ascii_lowercase),
            "<invalid>": ["<character><maybe_character>"],
            "<maybe_character>": ["<character><maybe_character>", ""],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["abba", "abc"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return [str(input_str)]


@dataclass(repr=False)
class palindrome_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["hq", "abba", "abc"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["pjxcxjp"]
    passing_input = ["abba", "abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["h"]
    passing_input = ["abba", "abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["h"]
    passing_input = ["abc", "abba"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["qmoeeomq", "abba"]
    passing_input = ["abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["hq", "abba", "abc"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["hq"]
    passing_input = ["abba", "abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["h"]
    passing_input = ["abba", "abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["lezaq", "abc"]
    passing_input = ["abba"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class palindrome_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["h"]
    passing_input = ["abba", "abc"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class RemoveVowelAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Remove Vowel"
        self._implementation_function_name: str = "removeVowels"
        self.programs = [
            vowel_1,
            vowel_2,
            vowel_3,
            vowel_4,
            vowel_5,
            vowel_6,
            vowel_7,
            vowel_8,
            vowel_9,
            vowel_10,
        ]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return os.path.join(
            super().get_dir(), Path("problem_9_Remove-vowels-from-string")
        )

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<word><maybe_word>"],
            "<maybe_word>": [" <word><maybe_word>", ""],
            "<word>": ["<char><maybe_char>"],
            "<char>": list(string.ascii_lowercase),
            "<maybe_char>": ["<char><maybe_char>", ""],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["welcome to avicenna", "hello my name is martin"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return [str(input_str)]


@dataclass(repr=False)
class vowel_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = [" <$uo?.*>"]
    passing_input = ["welcome to avicenna", "hello my name is martin"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["<a long string>"]
    passing_input = ["welcome to avicenna", "hello my name is martin"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["eicm", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class vowel_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class SquareRootAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "SquareRoot"
        self._implementation_function_name: str = "floorSqrt"
        self.programs = [
            sqrt_1,
            sqrt_2,
            sqrt_3,
            sqrt_4,
            sqrt_5,
            sqrt_6,
            sqrt_7,
            sqrt_8,
            sqrt_9,
            sqrt_10,
        ]

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


@dataclass(repr=False)
class sqrt_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["2"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["6"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4"]
    passing_input = ["5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["6"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["6179767"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["3", "5"]
    passing_input = ["4"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["4"]
    passing_input = ["5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class sqrt_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["1"]
    passing_input = ["4", "5"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


class MergeStringsAssignmentBenchmarkRepository(StudentAssignmentRepository):
    def __init__(self):
        self.name: str = "Merge Strings"
        self._implementation_function_name: str = "merge"
        self.programs = [
            merge_1,
            merge_2,
            merge_3,
            merge_4,
            merge_5,
            merge_6,
            merge_7,
            merge_8,
            merge_9,
            merge_10,
        ]

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
        s1, s2 = map(str, str(input_str).strip().split())
        return s1, s2


@dataclass(repr=False)
class merge_1(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Bye Hello"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_2(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_3(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX", "abc def", "hello bye"]
    passing_input = []

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_4(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["TjR GxPRYtwyy"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_5(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_6(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_7(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["rvcGbk QUWNOV", "abc def"]
    passing_input = ["hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_8(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_9(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input


@dataclass(repr=False)
class merge_10(StudentAssignmentBenchmarkProgram):
    name: str
    bug_id: int
    grammar: Grammar

    oracle: Callable
    failing_input = ["Qh eyNFX"]
    passing_input = ["abc def", "hello bye"]

    def get_initial_inputs(self) -> List[str]:
        return self.failing_input + self.passing_input
