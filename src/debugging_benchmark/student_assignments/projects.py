from typing import List, Sequence, Any
from pathlib import Path
from dataclasses import dataclass
import os
from abc import ABC

from debugging_framework.types import Grammar
from debugging_framework.types import HarnessFunctionType
from debugging_benchmark.student_assignments.grammars import *


class StudentAssignmentProject:
    def __init__(
        self,
        name: str,
        function_name: str,
        path_to_program: Path,
        grammar: Grammar = None,
        failing_inputs: List[str] = None,
        passing_inputs: List[str] = None,
        harness_function: HarnessFunctionType = None,
    ):
        self.grammar = grammar
        self.failing_inputs = failing_inputs
        self.passing_inputs = passing_inputs
        self.harness_function: HarnessFunctionType = (
            harness_function if harness_function else self.harness_function
        )

        self.name = name
        self.function_name = function_name
        self.path_to_program = path_to_program

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        param = list(map(int, str(input_str).strip().split()))
        return param

    @staticmethod
    def get_base_dir() -> Path:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        return Path(repo_dir) / Path("resources")


class GCDStudentAssignmentProject(StudentAssignmentProject, ABC):
    def __init__(
        self,
        failing_inputs: List[str],
        passing_inputs: List[str],
        path: Path,
    ):
        super().__init__(
            name="GCD",
            function_name="gcd",
            path_to_program=path,
            grammar=two_numbers_grammar,
            failing_inputs=failing_inputs,
            passing_inputs=passing_inputs,
        )

    def get_dir(self) -> Path:
        return self.get_base_dir() / Path("problem_1_GCD")


@dataclass
class GCD1StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["43 38", "10 2", "4 4"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_1"),
        )


@dataclass
class GCD2StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["43 38"],
            passing_inputs=["10 2", "4 4"],
            path=super().get_dir() / Path("prog_2"),
        )


@dataclass
class GCD3StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["21 21", "4 4"],
            passing_inputs=["10 2"],
            path=super().get_dir() / Path("prog_3"),
        )


@dataclass
class GCD4StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["21 38"],
            passing_inputs=["10 2", "4 4"],
            path=super().get_dir() / Path("prog_4"),
        )


@dataclass
class GCD5StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["43 38"],
            passing_inputs=["10 2", "4 4"],
            path=super().get_dir() / Path("prog_5"),
        )


@dataclass
class GCD6StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["21 21", "4 4"],
            passing_inputs=["10 2"],
            path=super().get_dir() / Path("prog_6"),
        )


@dataclass
class GCD7StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["43 38", "10 2"],
            passing_inputs=["4 4"],
            path=super().get_dir() / Path("prog_7"),
        )


@dataclass
class GCD8StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["1940673456000 194067"],
            passing_inputs=["10 2", "4 4"],
            path=super().get_dir() / Path("prog_8"),
        )


@dataclass
class GCD9StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["8 80", "4 4"],
            passing_inputs=["10 2"],
            path=super().get_dir() / Path("prog_9"),
        )


@dataclass
class GCD10StudentAssignmentProject(GCDStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["8 80", "10 2"],
            passing_inputs=["4 4"],
            path=super().get_dir() / Path("prog_10"),
        )


class SieveOfEratosthenesStudentAssignmentProject(StudentAssignmentProject, ABC):
    def __init__(
        self,
        failing_inputs: List[str],
        passing_inputs: List[str],
        path: Path,
    ):
        super().__init__(
            name="Sieve-of-Eratosthenes",
            function_name="sieveOfEratosthenes",
            path_to_program=path,
            grammar=single_number_grammar,
            failing_inputs=failing_inputs,
            passing_inputs=passing_inputs,
        )

    def get_dir(self) -> Path:
        return self.get_base_dir() / Path("problem_2_Sieve-of-Eratosthenes")


@dataclass
class SieveOfEratosthenes1StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["10000"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_1"),
        )


@dataclass
class SieveOfEratosthenes2StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7507"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_2"),
        )


@dataclass
class SieveOfEratosthenes3StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["4272", "10"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_3"),
        )


@dataclass
class SieveOfEratosthenes4StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["4272", "10"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_4"),
        )


@dataclass
class SieveOfEratosthenes5StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["4272", "10"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_5"),
        )


@dataclass
class SieveOfEratosthenes6StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7507"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_6"),
        )


@dataclass
class SieveOfEratosthenes7StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_7"),
        )


@dataclass
class SieveOfEratosthenes8StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_8"),
        )


@dataclass
class SieveOfEratosthenes9StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_9"),
        )


@dataclass
class SieveOfEratosthenes10StudentAssignmentProject(
    SieveOfEratosthenesStudentAssignmentProject
):
    def __init__(self):
        super().__init__(
            failing_inputs=["7"],
            passing_inputs=["10"],
            path=super().get_dir() / Path("prog_10"),
        )


class NPrStudentAssignmentProject(StudentAssignmentProject, ABC):
    def __init__(
        self,
        failing_inputs: List[str],
        passing_inputs: List[str],
        path: Path,
    ):
        super().__init__(
            name="nPr",
            function_name="nPr",
            path_to_program=path,
            grammar=two_numbers_grammar,
            failing_inputs=failing_inputs,
            passing_inputs=passing_inputs,
        )

    def get_dir(self) -> Path:
        return self.get_base_dir() / Path("problem_3_nPr")


@dataclass
class NPr1StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["8 8", "3 3"],
            passing_inputs=["2 1"],
            path=super().get_dir() / Path("prog_1"),
        )


@dataclass
class NPr2StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_2"),
        )


@dataclass
class NPr3StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4", "3 3"],
            passing_inputs=["2 1"],
            path=super().get_dir() / Path("prog_3"),
        )


@dataclass
class NPr4StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["7 6"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_4"),
        )


@dataclass
class NPr5StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_5"),
        )


@dataclass
class NPr6StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_6"),
        )


@dataclass
class NPr7StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_7"),
        )


@dataclass
class NPr8StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4"],
            passing_inputs=["2 1", "3 3"],
            path=super().get_dir() / Path("prog_8"),
        )


@dataclass
class NPr9StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["8 8", "3 3"],
            passing_inputs=["2 1"],
            path=super().get_dir() / Path("prog_9"),
        )


@dataclass
class NPr10StudentAssignmentProject(NPrStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["11 4", "3 3"],
            passing_inputs=["2 1"],
            path=super().get_dir() / Path("prog_10"),
        )


class FibonacciStudentAssignmentProject(StudentAssignmentProject, ABC):
    def __init__(
        self,
        failing_inputs: List[str],
        passing_inputs: List[str],
        path: Path,
    ):
        super().__init__(
            name="Fibonacci",
            function_name="nFibonacci",
            path_to_program=path,
            grammar=single_number_grammar,
            failing_inputs=failing_inputs,
            passing_inputs=passing_inputs,
        )

    def get_dir(self) -> Path:
        return self.get_base_dir() / Path("problem_4_Fibonacci_to_N")


@dataclass
class Fibonacci1StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["5"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_1"),
        )


@dataclass
class Fibonacci2StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["1000000000"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_2"),
        )


@dataclass
class Fibonacci3StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["1"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_3"),
        )


@dataclass
class Fibonacci4StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["1"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_4"),
        )


@dataclass
class Fibonacci5StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["5"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_5"),
        )


@dataclass
class Fibonacci6StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["1"],
            passing_inputs=[],
            path=super().get_dir() / Path("prog_6"),
        )


@dataclass
class Fibonacci7StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["4"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_7"),
        )


@dataclass
class Fibonacci8StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["5"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_8"),
        )


@dataclass
class Fibonacci9StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["5"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_9"),
        )


@dataclass
class Fibonacci10StudentAssignmentProject(FibonacciStudentAssignmentProject):
    def __init__(self):
        super().__init__(
            failing_inputs=["2"],
            passing_inputs=["1"],
            path=super().get_dir() / Path("prog_10"),
        )


# class NumberOfDivisorsAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "Number-of-Divisors"
#         self._implementation_function_name: str = "count_divisors"
#         self.programs = [
#             div_1,
#             div_2,
#             div_3,
#             div_4,
#             div_5,
#             div_6,
#             div_7,
#             div_8,
#             div_9,
#             div_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_5_Number-of-divisors"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<integer>"],
#             "<integer>": ["<one_nine><maybe_digits>"],
#             "<one_nine>": [str(num) for num in range(1, 10)],
#             "<digit>": list(string.digits),
#             "<maybe_digits>": ["", "<digits>"],
#             "<digits>": ["<digit>", "<digit><digits>"],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["6", "10"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         param = list(map(int, str(input_str).strip().split()))
#         return param
#
#
# @dataclass(repr=False)
# class div_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1", "6", "10"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["100000"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["7"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["30"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["18"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["6"]
#     passing_input = ["10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["18"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["7"]
#     passing_input = ["6", "10"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1", "10"]
#     passing_input = ["6"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class div_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1", "10"]
#     passing_input = ["6"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class BubbleSortAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "BubbleSort"
#         self._implementation_function_name: str = "bubbleSort"
#         self.programs = [
#             bubble_1,
#             bubble_2,
#             bubble_3,
#             bubble_4,
#             bubble_5,
#             bubble_6,
#             bubble_7,
#             bubble_8,
#             bubble_9,
#             bubble_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_6_Bubble-Sort"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<integer>\n<integer><maybe_integer>"],
#             "<integer>": ["<one_nine><maybe_digits>", "0"],
#             "<maybe_integer>": ["", " <integer><maybe_integer>"],
#             "<one_nine>": [str(num) for num in range(1, 10)],
#             "<digit>": list(string.digits),
#             "<maybe_digits>": ["", "<digits>"],
#             "<digits>": ["<digit>", "<digit><digits>"],
#         }
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         n = int(input_str.splitlines()[0])
#         arr = list(map(int, str(input_str.splitlines()[1]).strip().split()))
#         return arr, n
#
#
# @dataclass(repr=False)
# class bubble_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = [
#         "8\n24 18 38 43 14 40 1 54",
#         "10\n10 9 8 7 6 5 4 3 2 1"
#     ]
#     passing_input = ["5\n4 1 3 9 7", ]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54"]
#     passing_input = ["5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = ["5\n4 1 3 9 7"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["5\n91 23 32 74 6", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = ["5\n4 1 3 9 7"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "5\n4 1 3 9 7", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = ["5\n4 1 3 9 7"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = ["5\n4 1 3 9 7"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["8\n24 18 38 43 14 40 1 54", "10\n10 9 8 7 6 5 4 3 2 1"]
#     passing_input = ["5\n4 1 3 9 7"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class bubble_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = [
#         "8\n24 18 38 43 14 40 1 54",
#         "10\n10 9 8 7 6 5 4 3 2 1"
#     ]
#     passing_input = [
#         "5\n4 1 3 9 7"
#     ]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class MiddleAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "Middle"
#         self._implementation_function_name: str = "middle"
#         self.programs = [
#             middle_1,
#             middle_2,
#             middle_3,
#             middle_4,
#             middle_5,
#             middle_6,
#             middle_7,
#             middle_8,
#             middle_9,
#             middle_10
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_7_Middle-of-Three"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<first> <second> <third>"],
#             "<first>": ["<integer>"],
#             "<second>": ["<integer>"],
#             "<third>": ["<integer>"],
#             "<integer>": ["<one_nine><maybe_digits>"],
#             "<one_nine>": [str(num) for num in range(1, 10)],
#             "<digit>": list(string.digits),
#             "<maybe_digits>": ["", "<digits>"],
#             "<digits>": ["<digit>", "<digit><digits>"],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["978 518 300", "162 934 200"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         param = list(map(int, str(input_str).strip().split()))
#         return param
#
#
# @dataclass(repr=False)
# class middle_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["124 153 97", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["124 153 97", "978 518 300"]
#     passing_input = ["162 934 200"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["312 62 478", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["124 153 97", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["13 39 485", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["124 153 97", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["13 39 485"]
#     passing_input = ["978 518 300", "162 934 200"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["124 153 97", "978 518 300", "162 934 200"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["312 62 478", "162 934 200"]
#     passing_input = ["978 518 300"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class middle_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["459 8 20"]
#     passing_input = ["978 518 300", "162 934 200"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class PalindromeAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "Palindrome"
#         self._implementation_function_name: str = "isPalindrome"
#         self.programs = [
#             palindrome_1,
#             palindrome_2,
#             palindrome_3,
#             palindrome_4,
#             palindrome_5,
#             palindrome_6,
#             palindrome_7,
#             palindrome_8,
#             palindrome_9,
#             palindrome_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_8_Palindrome-String"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<valid>", "<invalid>"],
#             "<valid>": [
#                 "a<valid>a",
#                 "b<valid>b",
#                 "c<valid>c",
#                 "d<valid>d",
#                 "e<valid>e",
#                 "f<valid>f",
#                 "g<valid>g",
#                 "h<valid>h",
#                 "i<valid>i",
#                 "j<valid>j",
#                 "k<valid>k",
#                 "l<valid>l",
#                 "m<valid>m",
#                 "n<valid>n",
#                 "o<valid>o",
#                 "p<valid>p",
#                 "q<valid>q",
#                 "r<valid>r",
#                 "s<valid>s",
#                 "t<valid>t",
#                 "u<valid>u",
#                 "v<valid>v",
#                 "w<valid>w",
#                 "x<valid>x",
#                 "y<valid>y",
#                 "z<valid>z",
#                 "<character>",
#                 ""
#             ],
#             "<character>": list(string.ascii_lowercase),
#             "<invalid>": ["<character><maybe_character>"],
#             "<maybe_character>": ["<character><maybe_character>", ""],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["abba", "abc"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         return [str(input_str)]
#
#
# @dataclass(repr=False)
# class palindrome_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["hq", "abba", "abc"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["pjxcxjp"]
#     passing_input = ["abba", "abc"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["h"]
#     passing_input = ["abba", "abc"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["h"]
#     passing_input = ["abc", "abba"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["qmoeeomq", "abba"]
#     passing_input = ["abc"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["hq", "abba", "abc"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["hq", "abba", "abc"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["h"]
#     passing_input = ["abba", "abc"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["lezaq", "abc"]
#     passing_input = ["abba"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class palindrome_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["h"]
#     passing_input = ["abba", "abc"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class RemoveVowelAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "Remove Vowel"
#         self._implementation_function_name: str = "removeVowels"
#         self.programs = [
#             vowel_1,
#             vowel_2,
#             vowel_3,
#             vowel_4,
#             vowel_5,
#             vowel_6,
#             vowel_7,
#             vowel_8,
#             vowel_9,
#             vowel_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(
#             super().get_dir(), Path("problem_9_Remove-vowels-from-string")
#         )
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<word><maybe_word>"],
#             "<maybe_word>": [" <word><maybe_word>", ""],
#             "<word>": ["<char><maybe_char>"],
#             "<char>": list(string.printable),
#             "<maybe_char>": ["<char><maybe_char>", ""],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["welcome to avicenna", "hello my name is martin"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         return [str(input_str)]
#
#
# @dataclass(repr=False)
# class vowel_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = [" <$uo?.*>"]
#     passing_input = ["welcome to avicenna", "hello my name is martin"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     # failing_input = ["<a long string>"] # TODO fix this
#     failing_input = []
#     passing_input = ["welcome to avicenna", "hello my name is martin"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["eicm", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class vowel_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["&%^oq^", "welcome to avicenna", "hello my name is martin"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class SquareRootAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "SquareRoot"
#         self._implementation_function_name: str = "floorSqrt"
#         self.programs = [
#             sqrt_1,
#             sqrt_2,
#             sqrt_3,
#             sqrt_4,
#             sqrt_5,
#             sqrt_6,
#             sqrt_7,
#             sqrt_8,
#             sqrt_9,
#             sqrt_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_10_Square-root"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<integer>"],
#             "<integer>": ["<one_nine><maybe_digits>", "0"],
#             "<one_nine>": [str(num) for num in range(1, 10)],
#             "<digit>": list(string.digits),
#             "<maybe_digits>": ["", "<digits>"],
#             "<digits>": ["<digit>", "<digit><digits>"],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["4", "5"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         param = list(map(int, str(input_str).strip().split()))
#         return param
#
#
# @dataclass(repr=False)
# class sqrt_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["2"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["6"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["4"]
#     passing_input = ["5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["6"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["6179767"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["3", "5"]
#     passing_input = ["4"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["4"]
#     passing_input = ["5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class sqrt_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["1"]
#     passing_input = ["4", "5"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# class MergeStringsAssignmentBenchmarkRepository(StudentAssignmentRepository):
#     def __init__(self):
#         self.name: str = "Merge Strings"
#         self._implementation_function_name: str = "merge"
#         self.programs = [
#             merge_1,
#             merge_2,
#             merge_3,
#             merge_4,
#             merge_5,
#             merge_6,
#             merge_7,
#             merge_8,
#             merge_9,
#             merge_10,
#         ]
#
#     def get_implementation_function_name(self):
#         return self._implementation_function_name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_dir(self) -> Path:
#         return os.path.join(super().get_dir(), Path("problem_11_Merge-two-strings"))
#
#     @staticmethod
#     def get_grammar() -> Grammar:
#         return {
#             "<start>": ["<input>"],
#             "<input>": ["<word> <word>"],
#             "<word>": ["<character><maybe_character>"],
#             "<character>": list(string.printable),
#             "<maybe_character>": ["<character><maybe_character>", ""],
#         }
#
#     @staticmethod
#     def get_initial_inputs() -> List[str]:
#         return ["abc def", "hello bye"]
#
#     @staticmethod
#     def harness_function(input_str: str) -> Sequence[Any]:
#         s1, s2 = map(str, str(input_str).strip().split())
#         return s1, s2
#
#
# @dataclass(repr=False)
# class merge_1(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Bye Hello"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_2(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_3(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX", "abc def", "hello bye"]
#     passing_input = []
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_4(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["TjR GxPRYtwyy"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_5(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_6(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_7(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["rvcGbk QUWNOV", "abc def"]
#     passing_input = ["hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_8(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_9(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
#
#
# @dataclass(repr=False)
# class merge_10(StudentAssignmentBenchmarkProgram):
#     name: str
#     bug_id: int
#     grammar: Grammar
#
#     oracle: Callable
#     failing_input = ["Qh eyNFX"]
#     passing_input = ["abc def", "hello bye"]
#
#     def get_initial_inputs(self) -> List[str]:
#         return self.failing_input + self.passing_input
