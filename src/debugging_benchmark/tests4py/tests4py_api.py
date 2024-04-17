from typing import Callable, Union, Tuple, Optional
from pathlib import Path

from tests4py import api
from tests4py.projects import Project
from tests4py.api.test import RunReport
from tests4py.api.report import TestResult

from debugging_framework.input.input import Input
from debugging_framework.input.oracle import OracleResult
from debugging_framework.execution.expceptions import Tests4PySubjectException
from debugging_framework.types import HARNESS_FUNCTION


# Set default working directory
DEFAULT_WORK_DIR = Path("/tmp")


def build_project(
    project: Project, work_dir: Path = DEFAULT_WORK_DIR, buggy: bool = True
) -> None:
    """Build the given project."""
    project.buggy = buggy
    checkout_report = api.checkout(project, work_dir)
    assert checkout_report.successful
    compile_report = api.build(work_dir / project.get_identifier())
    assert compile_report.successful


def map_result(result: TestResult) -> OracleResult:
    """Map test result to Oracle result."""
    return {
        TestResult.FAILING: OracleResult.FAILING,
        TestResult.PASSING: OracleResult.PASSING,
        TestResult.UNDEFINED: OracleResult.UNDEFINED,
    }.get(result, OracleResult.UNDEFINED)


def run_project_from_dir(
    project_dir: Path, inp: Union[str, Input], harness_function: HARNESS_FUNCTION
) -> RunReport:
    """Run the project from the given directory with the provided input."""
    args = harness_function(inp)
    return api.run(project_dir, args, invoke_oracle=True)


def construct_oracle(
    project: Project,
    harness_function: HARNESS_FUNCTION,
    work_dir: Path = DEFAULT_WORK_DIR,
) -> Callable[[Union[str, Input]], Tuple[OracleResult, Optional[Exception]]]:
    """Construct an oracle for the given project."""

    def oracle(inp: Union[str, Input]) -> Tuple[OracleResult, Optional[Exception]]:
        project_dir = work_dir / project.get_identifier()
        report: RunReport = run_project_from_dir(
            project_dir, str(inp), harness_function=harness_function
        )
        exception = (
            Tests4PySubjectException("An Exception was triggered.")
            if report.test_result == TestResult.FAILING
            else None
        )
        # print("test_result:", report.test_result)
        # print("feedback:", report.feedback)
        # print("successful:", report.successful)
        # print("raised:", report.raised)
        result = (
            map_result(report.test_result)
            if report.successful
            else OracleResult.UNDEFINED
        )
        return result, exception

    return oracle
