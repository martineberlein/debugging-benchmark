from typing import List, Dict
from abc import ABC, abstractmethod

from debugging_framework.input.oracle import OracleResult
from debugging_framework.benchmark.program import BenchmarkProgram


class BenchmarkRepository(ABC):
    """
    Abstract base class representing a repository responsible for constructing BenchmarkProgram instances.

    A BenchmarkRepository acts as a factory that creates and configures instances of BenchmarkProgram,
    which are used to systematically evaluate various programs or code snippets within a defined testing
    or debugging framework.

    Subclasses of this abstract class should implement the `build` method to specify how BenchmarkPrograms
    are instantiated and configured based on error definitions and a default oracle.
    """

    @abstractmethod
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        """
        Constructs and returns a list of BenchmarkProgram instances based on provided error definitions
        and a default oracle.

        This method serves as a factory for creating benchmark programs, each configured with specific
        behavior patterns determined by the exceptions mapped to oracle results. The default oracle
        provides a fallback validation mechanism when no specific oracle is defined for an exception.

        :param Dict[Exception, OracleResult] err_def: A dictionary mapping exceptions to OracleResult
        instances, defining specific behaviors for handling various types of errors encountered during the execution
        of benchmark programs.
        :param OracleResult default_oracle: An OracleResult instance used as a default validation mechanism
        for any exceptions not explicitly covered in err_def.
        :return List[BenchmarkProgram]: A list of constructed and configured BenchmarkProgram instances.
        """
        raise NotImplementedError
