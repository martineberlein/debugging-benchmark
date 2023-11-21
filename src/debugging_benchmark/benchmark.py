#TODO: besseren namen finden
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Sequence, Any
from fuzzingbook.Grammars import Grammar

class BenchmarkProgram(ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_grammar(self):
        raise NotImplementedError

    @abstractmethod
    def get_initial_inputs(self):
        raise NotImplementedError

    @abstractmethod
    def get_oracle(self):
        raise NotImplementedError

    def to_dict(self):
        return {
            "grammar": self.get_grammar(),
            "oracle": self.get_oracle(),
            "initial_inputs": self.get_initial_inputs(),
        }

class BenchmarkRepository(ABC):
    @abstractmethod
    def get_dir(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        raise NotImplementedError

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
