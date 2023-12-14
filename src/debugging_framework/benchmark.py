import importlib.util
import sys
import ast

from typing import Union, List, Callable, Tuple, Set, Dict
from pathlib import Path
from abc import ABC, abstractmethod
from fuzzingbook.Grammars import Grammar
from fuzzingbook.Coverage import Coverage, Location, BranchCoverage

from debugging_framework.oracle import OracleResult


class BenchmarkProgram(ABC):
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
    def build(
            self,
            err_def: Dict[Exception, OracleResult] = None,
            default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        raise NotImplementedError

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


def load_module_dynamically(path: Union[str, Path]):
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
    module = load_module_dynamically(path)
    return getattr(module, object_name)


def load_function_from_class(path: Union[str, Path], function_name: str):
    class_name = get_class_name(path)
    class_ = load_object_dynamically(path, class_name)
    function = getattr(class_(), function_name)

    return function


def get_class_name(path: Union[str, Path]) -> str:
    # gets all class names in the file
    # TODO: encoding?
    data = Path(path).read_text()
    tree = ast.parse(data)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    # returns only the first class
    return classes[0]


def population_coverage(
    population: List[Tuple[int, int]], function: Callable
) -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        filtered_set = {
            (func, line)
            for (func, line) in cov.coverage()
            if "derivation_tree" not in func and "input" not in func
        }
        all_coverage |= filtered_set
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage


def population_branch_coverage(
    population: List[Tuple[int, int]], function: Callable
) -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with BranchCoverage() as cov:
            try:
                function(s)
            except:
                pass
        filtered_set = {
            (x, y)
            for (x, y) in cov.coverage()
            if "derivation_tree" not in x[0] and y[0] and "input" not in x[0] and y[0]
        }
        all_coverage |= filtered_set
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage
