import importlib.util
import sys
import ast

from typing import Union, List, Callable, Dict, Sequence, Any
from pathlib import Path
from abc import ABC, abstractmethod

from debugging_framework.types import Grammar
from debugging_framework.oracle import OracleResult


class BenchmarkProgram(ABC):
    """
    Gets constructed by BenchmarkRepositorys. Represents a single Problem/Program.
    """
    def __init__(
        self, name: str, grammar: Grammar, oracle: Callable, initial_inputs: List[str]
    ):
        self.name = name
        self.grammar = grammar
        self.oracle = oracle
        self.initial_inputs = initial_inputs

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_grammar(self) -> Grammar:
        raise NotImplementedError

    @abstractmethod
    def get_initial_inputs(self) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_oracle(self) -> Callable:
        raise NotImplementedError

    def to_dict(self):
        return {
            "grammar": self.get_grammar(),
            "oracle": self.get_oracle(),
            "initial_inputs": self.get_initial_inputs(),
        }


class BenchmarkRepository(ABC):
    """
    One Repository builds multiple BenchmarkPrograms.
    """
    name: str

    def __repr__(self):
        return f"BenchmarkRepository({self.name})"

    @abstractmethod
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
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

#TODO: Ist Module hier das richtige Wort?
def load_module_dynamically(path: Union[str, Path]):
    """ 
    Loads module from the provided path
    """
    # Step 1: Convert file path to module name
    file_path = ""
    if isinstance(path, Path):
        file_path = str(path.absolute())
    elif isinstance(path, str):
        file_path = str(path)
    else:
        raise TypeError("path should be from type Path or str")

    module_name = file_path.replace("/", ".").rstrip(".py")

    # Step 2: Load module dynamically
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def load_object_dynamically(path: Union[str, Path], object_name: str):
    """
    Loads Object from the Module provided by the Path
    """
    module = load_module_dynamically(path)
    return getattr(module, object_name)


def load_function_from_class(path: Union[str, Path], function_name: str) -> Callable:
    """
    Loads a function from a class
    """
    class_name = get_class_name(path)
    class_ = load_object_dynamically(path, class_name)
    function = getattr(class_(), function_name)

    return function


def get_class_name(path: Union[str, Path], encoding: str = 'utf-8', first_class: bool = True) -> str:
    """
    Gets all Classes provided by the file from the Path.

    :param encoding: encoding of the file specified by the path. defaults to utf-8
    :param first_class: If True only returns first found class otherwise returns all classes in file
    """
    data = Path(path).read_text(encoding=encoding)
    tree = ast.parse(data)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    if first_class:
        return classes[0]
    else:
        return classes

