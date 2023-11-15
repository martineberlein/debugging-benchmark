from abc import ABC, abstractmethod
from ast import literal_eval
from typing import Type, List, Callable, Dict, Sequence, Any
from pathlib import Path
import string
import os

from fuzzingbook.Grammars import Grammar

from debugging_framework.oracle import OracleResult
from debugging_framework.oracle_construction import construct_oracle
from debugging_framework.subjects import load_object_dynamically, BenchmarkProgram


class RefactoryBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        bug_id: int,
        grammar: Grammar,
        initial_inputs: List[str],
        oracle: Callable,
    ):
        self.name = name
        self.bug_id = bug_id
        self.grammar = grammar
        self.initial_inputs = initial_inputs
        self.oracle = oracle

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


class BenchmarkRepository(ABC):
    @abstractmethod
    def get_dir(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        raise NotImplementedError


class RefactoryBenchmarkRepository(BenchmarkRepository, ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError(
            "A Refactory-Benchmark-Repository needs to have a unique name."
        )

    @staticmethod
    def get_grammar() -> Grammar:
        raise NotImplementedError

    @staticmethod
    def get_initial_inputs() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_implementation_function_name(self):
        raise NotImplementedError

    def get_dir(self) -> Path:
        this_file_path_dir = os.path.dirname(os.path.abspath(__file__))
        return Path(this_file_path_dir) / Path("refactory")

    def get_ground_truth_location(self):
        return self.get_dir() / Path("code/reference/reference.py")

    def load_ground_truth(self):
        path_to_ground_truth = self.get_ground_truth_location()
        return load_object_dynamically(
            path_to_ground_truth,
            self.get_implementation_function_name()
        )

    def load_implementation(
        self, solution_type: str, formatted_bug_id: str
    ) -> Callable:
        path_to_dir = self.get_dir() / Path(f"code/{solution_type}")
        path_to_implementation = list(
            path_to_dir.resolve().glob(f"*{formatted_bug_id}.py")
        )[0]

        return load_object_dynamically(
            path_to_implementation,
            self.get_implementation_function_name(),
        )

    def _construct_test_program(
        self,
        bug_id: int,
        error_def: Dict[Type[Exception], OracleResult],
        default_oracle: OracleResult,
        solution_type: str,
    ) -> RefactoryBenchmarkProgram:
        formatted_bug_id = str(bug_id).zfill(3)
        ground_truth = self.load_ground_truth()
        program = self.load_implementation(solution_type, formatted_bug_id)

        oracle = construct_oracle(
            program,
            ground_truth,
            error_def,
            default_oracle_result=default_oracle,
            timeout=0.01,
            harness_function=self.harness_function,
        )

        return RefactoryBenchmarkProgram(
            name=self.get_name(),
            bug_id=bug_id,
            grammar=self.get_grammar(),
            initial_inputs=self.get_initial_inputs(),
            oracle=oracle,
        )

    def build(
        self,
        error_def: Dict[Type[Exception], OracleResult] = None,
        default_oracle: OracleResult = None,
        solution_type: str = "wrong",
    ) -> List[RefactoryBenchmarkProgram]:
        path_to_subjects = self.get_dir() / Path(f"code/{solution_type}")
        number_of_subjects = len(list(path_to_subjects.resolve().glob(f"*.py")))

        constructed_test_programs: List[RefactoryBenchmarkProgram] = []
        for bug_id in range(1, number_of_subjects):
            try:
                subject = self._construct_test_program(
                    bug_id, error_def, default_oracle, solution_type
                )
                constructed_test_programs.append(subject)
            except Exception as e:
                print(f"Subject {str(bug_id)} could not be build.")

        return constructed_test_programs

    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass

class Question1RefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "RefactoryQ1"
        self._implementation_function_name: str = "search"

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_1")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<first>, <second>"],
            "<first>": ["<integer>"],
            "<second>": [
                "()",
                "[]",
                "(<integer>, <integer><list>)",
                "[<integer><list>]",
            ],
            "<list>": ["", ", <integer><list>"],
            "<integer>": ["<maybe_minus><one_nine><maybe_digits>"],
            "<maybe_minus>": ["", "-"],  #
            "<one_nine>": [str(num) for num in range(1, 10)],
            "<digit>": list(string.digits),
            "<maybe_digits>": ["", "<digits>"],
            "<digits>": ["<digit>", "<digit><digits>"],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["42, (-5, 1, 3, 5, 7, 10)", "3, (1, 5, 10)"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        # Split the string into two parts based on the first comma and a space
        arg1_str, arg2_str = input_str.split(", ", 1)

        # Convert the string parts to Python literals
        arg1 = literal_eval(arg1_str)
        arg2 = literal_eval(arg2_str)

        return arg1, arg2


def main():
    repo = Question1RefactoryBenchmarkRepository()
    subjects: List[RefactoryBenchmarkProgram] = repo.build(solution_type="wrong")
    for subject in subjects:
        print(subject.name, subject.bug_id)
        param = subject.to_dict()
        oracle = param.get("oracle")
        inputs = param.get("initial_inputs")
        for inp in inputs:
            print(oracle(inp))


if __name__ == "__main__":
    main()
