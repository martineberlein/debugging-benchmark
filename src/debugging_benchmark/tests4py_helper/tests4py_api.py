from typing import List, Callable, Union, Tuple, Optional
from pathlib import Path
import logging
import shlex

from tests4py import api, logger
from tests4py.projects import Project
from tests4py.api.test import RunReport
from tests4py.api.report import TestResult

from debugging_framework.input import Input
from debugging_framework.oracle import OracleResult
from debugging_framework.expceptions import Tests4PySubjectException


# Set default working directory
DEFAULT_WORK_DIR = Path("/tmp")


def get_test_arguments(inp: Union[str, Input]) -> List[str]:
    """Parse input into a list of arguments."""
    parts = shlex.split(str(inp))
    return [part for part in parts if part]


def build_project(
    project: Project, work_dir: Path = DEFAULT_WORK_DIR, buggy: bool = True
) -> None:
    """Build the given project."""
    project.buggy = buggy
    checkout_report = api.checkout_project(project, work_dir)
    assert checkout_report.successful
    compile_report = api.compile_project(work_dir / project.get_identifier())
    assert compile_report.successful


def run_project(project: Project, work_dir: Path, inp: Union[str, Input]) -> RunReport:
    """Run the given project with the provided input."""
    project_dir = work_dir / project.get_identifier()
    return run_project_from_dir(project_dir, inp)


def map_result(result: TestResult) -> OracleResult:
    """Map test result to Oracle result."""
    return {
        TestResult.FAILING: OracleResult.FAILING,
        TestResult.PASSING: OracleResult.PASSING,
        TestResult.UNDEFINED: OracleResult.UNDEFINED,
    }.get(result, OracleResult.UNDEFINED)


def run_project_from_dir(project_dir: Path, inp: Union[str, Input]) -> RunReport:
    """Run the project from the given directory with the provided input."""
    args = get_test_arguments(inp)
    # print(args)
    return api.run_project(project_dir, args, invoke_oracle=True)


def construct_oracle(
    project: Project, work_dir: Path = DEFAULT_WORK_DIR
) -> Callable[[Union[str, Input]], Tuple[OracleResult, Optional[Exception]]]:
    """Construct an oracle for the given project."""

    def oracle(inp: Union[str, Input]) -> Tuple[OracleResult, Optional[Exception]]:
        project_dir = work_dir / project.get_identifier()
        report: RunReport = run_project_from_dir(project_dir, inp)
        exception = (
            Tests4PySubjectException(report.feedback)
            if report.feedback
            else None
        )
        print("test_result:", report.test_result)
        print("feedback:", report.feedback)
        print("successful:", report.successful)
        print("raised:", report.raised)
        result = map_result(report.test_result) if report.successful else OracleResult.UNDEFINED
        return (
            result,
            exception
        )

    return oracle


def pysnooper_2_test():
    """Test for the pysnooper_2 project."""
    project: Project = api.pysnooper_2
    # build_project(project)
    oracle = construct_oracle(project)
    assert oracle("-otest.log\n-cint=str") == OracleResult.FAILING
    assert oracle("-d1\n-T") == OracleResult.PASSING
    assert oracle("-aTest") == OracleResult.UNDEFINED


def middle_1_test():
    """Test for the middle_1 project."""
    project: Project = api.middle_1
    build_project(project)
    oracle = construct_oracle(project)
    assert oracle("2 1 3") == OracleResult.FAILING
    assert oracle("1 2 3") == OracleResult.PASSING
    assert oracle("1 2") == OracleResult.UNDEFINED


def youtubedl_1_test():
    """Test for the middle_1 project."""
    project: Project = api.youtubedl_1
    build_project(project)
    oracle = construct_oracle(project)
    assert oracle("-q !is_live\n-d {\\'is_live\\':False}") == OracleResult.FAILING
    assert oracle("-q \\'test>?0\\'\n-d {}") == OracleResult.PASSING
    #assert oracle("1 2") == OracleResult.UNDEF


if __name__ == "__main__":
    logger.LOGGER.setLevel(logging.ERROR)

    # Run tests
    #pysnooper_2_test()
    middle_1_test()
    #youtubedl_1_test()
