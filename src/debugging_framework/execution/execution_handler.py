from abc import ABC, abstractmethod
from typing import Union, Optional, Set, List, Tuple

from debugging_framework.input.input import Input
from debugging_framework.input.oracle import OracleResult
from debugging_framework.execution.report import TResultMonad, Report
from debugging_framework.types import OracleType, BatchOracleType


class ExecutionHandler(ABC):
    """
    Abstract base class for handling the execution of test inputs and integrating the results into a report.
    This class provides the core functionality and interface for executing inputs and processing the results
    using a specified oracle that determines the result of each test input.
    """

    def __init__(self, oracle: OracleType | BatchOracleType):
        """
        Initializes the ExecutionHandler with a specific oracle.
        :param OracleType oracle: The oracle used to evaluate test inputs.
        """
        self.oracle = oracle

    @staticmethod
    def map_result(result: OracleResult) -> bool:
        """
        Maps an OracleResult to a boolean value indicating whether the result is a failing case.

        :param OracleResult result: The result from the oracle to be mapped.
        :return bool: True if the result is `FAILING`, False otherwise (both `PASSING` and `UNDEFINED`).
        """
        match result:
            case OracleResult.FAILING:
                return True
            case OracleResult.PASSING | OracleResult.UNDEFINED:
                return False

    @staticmethod
    def add_to_report(
        report: Report, test_input: Union[Input, str], exception: Optional[Exception]
    ):
        """
        Adds a failure entry to the report based on the test input and any exception encountered during processing.
        :param Report report: The report to which the failure will be added.
        :param Union[Input, str] test_input: The test input that resulted in failure.
        :param Optional[Exception] exception: The exception encountered during the execution of the input, if any.
        """
        report.add_failure(test_input, exception)

    @abstractmethod
    def label(self, test_inputs: Set[Input], report: Report):
        """
        Processes a set of test inputs, evaluates them using the oracle, and updates the report based on the results.
        :param Set[Input] test_inputs: The set of inputs to be processed.
        :param Report report: The report where results will be recorded.
        """
        raise NotImplementedError


class SingleExecutionHandler(ExecutionHandler):
    """
    Handles the execution of individual test inputs serially, applying an oracle to each input and updating the report.
    Inherits from ExecutionHandler.
    """

    def _get_label(self, test_input: Union[Input, str]) -> TResultMonad:
        """
        Applies the oracle to a single test input and returns the result wrapped in a TResultMonad.
        :param Union[Input, str] test_input: The test input to be evaluated.
        :return TResultMonad: The result of the oracle evaluation.
        """
        return TResultMonad(self.oracle(test_input))

    def label(self, test_inputs: Set[Input], report: Report):
        """
        Labels each input in a set individually, updates the input's oracle attribute, and reports failures if any.
        :param Set[Input] test_inputs: The set of inputs to be processed.
        :param Report report: The report where results will be recorded.
        """
        for inp in test_inputs:
            label, exception = self._get_label(inp).value()
            inp.oracle = label
            if self.map_result(label):
                self.add_to_report(report, inp, exception)

    def label_strings(self, test_inputs: Set[str], report: Report):
        """
        Handles a set of string inputs, evaluates them, and updates the report accordingly.
        :param Set[str] test_inputs: The set of string inputs to be processed.
        :param Report report: The report where results will be recorded.
        """
        for inp in test_inputs:
            label, exception = self._get_label(inp).value()
            if self.map_result(label):
                self.add_to_report(report, inp, exception)


class BatchExecutionHandler(ExecutionHandler):
    """
    Handles the batch execution of test inputs, applying the oracle to all inputs simultaneously
    and updating the report.
    Inherits from ExecutionHandler.
    """

    def _get_label(self, test_inputs: Set[Input]) -> List[Tuple[Input, TResultMonad]]:
        """
        Applies the oracle to a set of test inputs and returns the results as a list of tuples, each containing
        the input and its TResultMonad.
        :param Set[Input] test_inputs: The set of inputs to be evaluated.
        :return List[Tuple[Input, TResultMonad]]: A list of tuples pairing each input with its TResultMonad result.
        """
        results = self.oracle(test_inputs)
        return [
            (inp, TResultMonad(result)) for inp, result in zip(test_inputs, results)
        ]

    def label(self, test_inputs: Set[Input], report: Report):
        """
        Processes a set of test inputs in batch, evaluates them using the oracle,
        and updates the report based on the results.
        :param Set[Input] test_inputs: The set of inputs to be processed.
        :param Report report: The report where results will be recorded.
        """
        test_results = self._get_label(test_inputs)
        for inp, test_result in test_results:
            label, exception = test_result.value()
            inp.oracle = label
            if self.map_result(label):
                self.add_to_report(report, inp, exception)
