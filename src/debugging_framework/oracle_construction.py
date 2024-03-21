from typing import Callable, Dict, Type, Optional, Tuple, Any, Sequence

from copy import deepcopy

from debugging_framework.oracle import OracleResult
from debugging_framework.input import Input
from debugging_framework.timeout_manager import ManageTimeout
from debugging_framework.expceptions import UnexpectedResultError
from debugging_framework.memory_manager import ManageMemory

import contextlib


def execute_program(program_, param: Sequence, timeout) -> Any:
    with ManageTimeout(timeout):
        # silencing the stdout for PuT
        with contextlib.redirect_stdout(None):
            dp = deepcopy(param)
            return program_(*dp)


def construct_oracle(
        program_under_test: Callable,
        program_oracle: Optional[Callable],
        error_definitions: Optional[Dict[Type[Exception], OracleResult]] = None,
        timeout: float = 1,
        default_oracle_result: OracleResult = OracleResult.UNDEFINED,
        harness_function: Callable = None,
) -> Callable[[Input], Tuple[OracleResult, Optional[Exception]]]:
    error_definitions = error_definitions or {}
    default_oracle_result = (
        OracleResult.FAILING if not error_definitions else default_oracle_result
    )

    if not isinstance(error_definitions, dict):
        raise ValueError(f"Invalid value for expected_error: {error_definitions}")

    params = locals()

    # Choose oracle construction method based on presence of program_oracle
    if program_oracle:
        oracle_constructor = _construct_functional_oracle
    else:
        oracle_constructor = _construct_failure_oracle
        params.pop("program_oracle")

    return oracle_constructor(**params)


def _construct_functional_oracle(
        program_under_test: Callable,
        program_oracle: Callable,
        error_definitions: Dict[Type[Exception], OracleResult],
        timeout: float,
        default_oracle_result: OracleResult,
        harness_function: Callable,
):
    def oracle(inp: Input) -> Tuple[OracleResult, Optional[Exception]]:
        # param = list(map(int, str(inp).strip().split()))  # This might become a problem
        param = harness_function(str(inp)) if harness_function else str(inp)

        try:
            produced_result = execute_program(program_under_test, param, timeout)
            expected_result = execute_program(program_oracle, param, timeout)

            if (expected_result != produced_result) or (type(expected_result) is not type(produced_result)):
                raise UnexpectedResultError("Results do not match")
        except Exception as e:
            return error_definitions.get(type(e), default_oracle_result), e
        return OracleResult.PASSING, None

    return oracle


def _construct_failure_oracle(
        program_under_test: Callable,
        error_definitions: Dict[Type[Exception], OracleResult],
        timeout: float,
        default_oracle_result: OracleResult,
        harness_function: Callable,
):
    def oracle(inp: Input) -> Tuple[OracleResult, Optional[Exception]]:
        param = harness_function(str(inp)) if harness_function else str(inp)
        try:
            with ManageTimeout(timeout):
                # silencing the stdout for PuT
                with contextlib.redirect_stdout(None):
                    program_under_test(*param)
        except Exception as e:
            return error_definitions.get(type(e), default_oracle_result), e
        return OracleResult.PASSING, None

    return oracle
