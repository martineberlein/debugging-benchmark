from typing import List, Dict, Any
from abc import ABC
import dill as pickle

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

    def to_dict(self, only_passing: bool = False) -> Dict[str, Any]:
        """
        Serializes essential elements of the program to a dictionary, optionally filtering for only passing inputs.
        :param bool only_passing: If True, the dictionary includes only passing inputs under 'initial_inputs'.
                                  If False, it includes all initial inputs. Defaults to False.
        :return Dict[str, Any]: A dictionary with keys 'grammar', 'oracle', and 'initial_inputs'. The 'initial_inputs'
                                key contains either all initial inputs or only those that are passing, based on the
                                value of the `only_passing` parameter.
        """
        return {
            "grammar": self.get_grammar(),
            "oracle": self.get_oracle(),
            "initial_inputs": self.get_passing_inputs() if only_passing else self.get_initial_inputs(),
        }

    def dump(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)