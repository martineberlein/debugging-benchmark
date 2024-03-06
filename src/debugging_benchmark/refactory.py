from abc import ABC, abstractmethod
from ast import literal_eval
from typing import Type, List, Callable, Dict, Sequence, Any
from pathlib import Path
import string
import os

from debugging_framework.types import Grammar
from debugging_framework.oracle import OracleResult
from debugging_framework.oracle_construction import construct_oracle
from debugging_framework.benchmark import load_object_dynamically
from debugging_framework.benchmark import BenchmarkProgram, BenchmarkRepository


class RefactoryBenchmarkProgram(BenchmarkProgram):
    def __init__(
        self,
        name: str,
        implementation_function_name: str,
        bug_id: int,
        grammar: Grammar,
        initial_inputs: List[str],
        oracle: Callable,
    ):
        super().__init__(name, grammar, oracle, initial_inputs)
        self.bug_id = bug_id
        self.implementation_function_name = implementation_function_name

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


class RefactoryBenchmarkRepository(BenchmarkRepository, ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError(
            "A Refactory-Benchmark-Repository needs to have a unique name."
        )
    #waren vorher nicht vorhanden aber tests sind durchgelaufen??? Aber Linter sagt gibt probleme
    @abstractmethod
    def get_implementation_function_name(self) -> List[str]:
        raise NotImplementedError(
            "Every Question has a unique implementation function name"
        )
    #waren vorher nicht vorhanden aber tests sind durchgelaufen???
    @staticmethod
    @abstractmethod    
    def harness_function(input_str: str) -> Sequence[Any]:
            raise NotImplementedError(
                "Every Question has a unique harness function"
            )
        
    def get_dir(self) -> Path:
        this_file_path_dir = os.path.dirname(os.path.abspath(__file__))
        return Path(this_file_path_dir) / Path("refactory")
    
    def get_ground_truth_location(self):
        return self.get_dir() / Path("code/reference/reference.py")

    def load_ground_truth(self, implementation_function_name: str):
        path_to_ground_truth = self.get_ground_truth_location()
        return load_object_dynamically(
            path_to_ground_truth,
            implementation_function_name
        )

    def load_implementation(
        self, solution_type: str, formatted_bug_id: str, implementation_function_name: str
    ) -> Callable:
        path_to_dir = self.get_dir() / Path(f"code/{solution_type}")
        path_to_implementation = list(
            path_to_dir.resolve().glob(f"*{formatted_bug_id}.py")
        )[0]
    
        return load_object_dynamically(
            path_to_implementation,
            implementation_function_name,
        )

    def _construct_test_program(
        self,
        bug_id: int,
        implementation_function_name: str,
        error_def: Dict[Type[Exception], OracleResult],
        default_oracle: OracleResult,
        solution_type: str,
    ) -> RefactoryBenchmarkProgram:
        formatted_bug_id = str(bug_id).zfill(3)
        ground_truth = self.load_ground_truth(implementation_function_name)
        program = self.load_implementation(solution_type, formatted_bug_id, implementation_function_name)

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
            implementation_function_name=implementation_function_name,
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
                for implementation_function_name in self.get_implementation_function_name():
                    subject = self._construct_test_program(
                        bug_id, implementation_function_name, error_def, default_oracle, solution_type
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
        self._implementation_function_name: str = ["search"]

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
    
#Problem: es gibt 3 function names
class Question2aRefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "RefactoryQ2a"
        self._implementation_function_name: List[str] = ["unique_day"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_2")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<day>, <possible_birthdays>"],
            "<day>": [str(num) for num in range(1, 32)],
            "<possible_birthdays>": [
                "<birthday>",
                "<birthday>; <possible_birthdays>"
            ],
            "<birthday>": [
                "(<month>, <day>)"
            ],
            "<month>": [
                "January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"
            ],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["24, (August, 22); (January, 4)", "8, (June, 11); (November, 31)"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        # Split the string into two parts based on the first comma and a space
        arg1, arg2 = input_str.split(", ", 1)

        tuples = arg2.split("; ")
        literal_tuples = []
        for t in tuples:
            print(t)
            print(type(t))
            literal_tuple = literal_eval(t)
            literal_tuples.append(literal_tuple)
        
        return arg1, literal_tuples
    
class Question2bRefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "RefactoryQ2b"
        self._implementation_function_name: List[str] = ["unique_month"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_2")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<month>, <possible_birthdays>"],
            "<day>": [str(num) for num in range(1, 32)],
            "<possible_birthdays>": [
                "<birthday>",
                "<birthday>; <possible_birthdays>"
            ],
            "<birthday>": [
                "(<month>, <day>)"
            ],
            "<month>": [
                "January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"
            ],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["November, (April, 3)", "July, (October, 17); (December, 19); (April, 27); (January, 4)"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        # Split the string into two parts based on the first comma and a space
        arg1, arg2 = input_str.split(", ", 1)
        
        tuples = arg2.split("; ")
        return arg1, tuples

#Könnte man mit 2b zsmfassen da beide den gleichen Input brauchen
#Allerdings wird hier nur ein monat betrachtet vllt doch nochmal grammar anpassen 
class Question2cRefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "RefactoryQ2c"
        self._implementation_function_name: List[str] = ["contains_unique_day"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_2")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<month>, <possible_birthdays>"],
            "<day>": [str(num) for num in range(1, 32)],
            "<possible_birthdays>": [
                "<birthday>",
                "<birthday>; <possible_birthdays>"
            ],
            "<birthday>": [
                "(<month>, <day>)"
            ],
            "<month>": [
                "January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"
            ],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["November, (April, 3)", "July, (October, 17); (December, 19); (April, 27); (January, 4)"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        # Split the string into two parts based on the first comma and a space
        arg1, arg2 = input_str.split(", ", 1)
        
        tuples = arg2.split("; ")
        return arg1, tuples

class Question3RefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "Refactory3"
        self._implementation_function_name: List[str] = ["remove_extras"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_3")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<one_nine>, <one_nine><list>"],
            "<list>": ["", ", <one_nine><list>"],
            "<one_nine>": [str(num) for num in range(1, 10)],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["1, 2, 3, 4", "1, 1, 1, 2"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return input_str.split(", ")
    

class Question4RefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "Refactory4"
        self._implementation_function_name: List[str] = ["sort_age"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_4")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<person>; <person><list>"],
            "<list>": ["", "; <person>"],
            "<person>": ["(<gender>, <age>)"],
            "<gender>": ["male", "female"],
            "<age>": [str(num) for num in range(1, 101)],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["(female, 57); (female, 83); (female, 14)", "(female, 99); (male, 77)"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        return input_str.split("; ")
    
class Question5RefactoryBenchmarkRepository(RefactoryBenchmarkRepository):
    def __init__(self):
        self.name: str = "Refactory5"
        self._implementation_function_name: List[str] = ["top_k"]

    def get_implementation_function_name(self):
        return self._implementation_function_name

    def get_name(self) -> str:
        return self.name

    def get_dir(self) -> Path:
        return super().get_dir() / Path("./question_5")

    @staticmethod
    def get_grammar() -> Grammar:
        return {
            "<start>": ["<input>"],
            "<input>": ["<integer>, <integer>, <integer>, <integer><list>; <k>"],
            "<k>": [str(num) for num in range (1,4)],
            "<list>": ["", ", <integer><list>"],
            "<integer>": ["<maybe_minus><one_nine><maybe_digits>"],
            "<maybe_minus>": ["", "-"],  
            "<one_nine>": [str(num) for num in range(1, 10)],
            "<digit>": list(string.digits),
            "<maybe_digits>": ["", "<digits>"],
            "<digits>": ["<digit>", "<digit><digits>"],
        }

    @staticmethod
    def get_initial_inputs() -> List[str]:
        return ["-6, -2, 6701, 35; 2", "-6, 6, -9, -8, -2; 3"]

    @staticmethod
    def harness_function(input_str: str) -> Sequence[Any]:
        numbers, k = input_str.split("; ")
        numbers_splitted = numbers.split(", ")
        return numbers_splitted, k