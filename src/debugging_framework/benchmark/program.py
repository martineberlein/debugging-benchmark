from typing import List, Dict, Any
from abc import ABC

from debugging_framework.types import OracleType
from debugging_framework.types import Grammar


class BenchmarkProgram(ABC):
    """
    Gets constructed by BenchmarkRepositories. Represents a single Problem/Program.
    """

    def __init__(
        self,
        name: str,
        grammar: Grammar,
        oracle: OracleType,
        failing_inputs: List[str],
        passing_inputs: List[str],
    ):
        self.name = name
        self.grammar = grammar
        self.oracle = oracle
        self.failing_inputs = failing_inputs
        self.passing_inputs = passing_inputs

    def __repr__(self):
        return f"BenchmarkProgram({self.name})"

    def get_name(self) -> str:
        """
        Retrieves the name of the program.
        :return str: The name of the program.
        """
        return self.name

    def get_grammar(self) -> Grammar:
        """
        Retrieves the grammar associated with the program.
        :return Grammar: The grammar of the program.
        """
        return self.grammar

    def get_failing_inputs(self) -> List[str]:
        """
        Retrieves the list of failing input cases.
        :return List[str]: The failing input cases.
        """
        return self.failing_inputs

    def get_passing_inputs(self) -> List[str]:
        """
        Retrieves the list of passing input cases.
        :return List[str]: The passing input cases.
        """
        return self.passing_inputs

    def get_initial_inputs(self) -> List[str]:
        """
        Retrieves the list of initial inputs used for testing the program.
        :return List[str]: The initial input cases.
        """
        return self.passing_inputs + self.failing_inputs

    def get_oracle(self) -> OracleType:
        """
        Retrieves the oracle callable used to validate program outputs.
        :return Callable: The oracle function.
        """
        return self.oracle

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes essential elements of the program to a dictionary.
        :return Dict[str, Any]: The dictionary containing grammar, oracle, and initial inputs.
        """
        return {
            "grammar": self.get_grammar(),
            "oracle": self.get_oracle(),
            "initial_inputs": self.get_initial_inputs(),
        }
