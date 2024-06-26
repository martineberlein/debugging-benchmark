from typing import List, Dict, Callable
from pathlib import Path
from abc import ABC
import os

from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.student_assignments.program import (
    StudentAssignmentBenchmarkProgram,
)
from debugging_framework.benchmark.loader import load_function_from_class
import debugging_benchmark.student_assignments.projects as sap_projects
from debugging_framework.input.oracle_construction import FunctionalOracleConstructor


class StudentAssignmentRepository(BenchmarkRepository, ABC):
    def __init__(self, projects: List[sap_projects.StudentAssignmentProject]):
        """
        Initializes the repository with a list of StudentAssignmentProject instances.
        :param List[StudentAssignmentProject] projects: The projects to be included in the benchmark repository.
        """
        self.projects = projects

    @staticmethod
    def get_ground_truth_location(
        project: sap_projects.StudentAssignmentProject,
    ) -> Path:
        base_dir = project.get_dir()
        return base_dir / Path("reference1.py")

    def load_ground_truth(self, project: sap_projects.StudentAssignmentProject):
        path_to_ground_truth = self.get_ground_truth_location(project)
        return load_function_from_class(path_to_ground_truth, project.function_name)

    @staticmethod
    def load_implementation(project: sap_projects.StudentAssignmentProject) -> Callable:
        path_to_implementation = os.path.join(project.path_to_program, Path("buggy.py"))
        return load_function_from_class(path_to_implementation, project.function_name)

    def _construct_test_program(
        self,
        project: sap_projects.StudentAssignmentProject,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = OracleResult.UNDEFINED,
    ) -> StudentAssignmentBenchmarkProgram:
        ground_truth = self.load_ground_truth(project=project)
        program = self.load_implementation(project=project)

        oracle = FunctionalOracleConstructor(
            program=program,
            program_oracle=ground_truth,
            error_definitions=err_def,
            default_oracle_result=default_oracle,
            timeout=0.01,
            harness_function=project.harness_function,
        ).build()

        return StudentAssignmentBenchmarkProgram(
            name=str(project),
            grammar=project.grammar,
            oracle=oracle,
            failing_inputs=project.failing_inputs,
            passing_inputs=project.passing_inputs,
        )

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = OracleResult.UNDEFINED,
    ) -> List[StudentAssignmentBenchmarkProgram]:
        constructed_programs: List[StudentAssignmentBenchmarkProgram] = []
        for project in self.projects:
            try:
                program = self._construct_test_program(
                    project=project,
                    err_def=err_def,
                    default_oracle=default_oracle,
                )
                constructed_programs.append(program)
            except Exception as e:
                print(f"Subject {project.__name__} could not be built.")
                print(e)

        return constructed_programs


class GCDStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.GCD1StudentAssignmentProject(),
            sap_projects.GCD2StudentAssignmentProject(),
            sap_projects.GCD3StudentAssignmentProject(),
            sap_projects.GCD4StudentAssignmentProject(),
            sap_projects.GCD5StudentAssignmentProject(),
            sap_projects.GCD6StudentAssignmentProject(),
            sap_projects.GCD7StudentAssignmentProject(),
            sap_projects.GCD8StudentAssignmentProject(),
            sap_projects.GCD9StudentAssignmentProject(),
            sap_projects.GCD10StudentAssignmentProject(),
        ]
        super().__init__(projects)


class SieveOfEratosthenesStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.SieveOfEratosthenes1StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes2StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes3StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes4StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes5StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes6StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes7StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes8StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes9StudentAssignmentProject(),
            sap_projects.SieveOfEratosthenes10StudentAssignmentProject(),
        ]
        super().__init__(projects)


class NPrStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.NPr1StudentAssignmentProject(),
            sap_projects.NPr2StudentAssignmentProject(),
            sap_projects.NPr3StudentAssignmentProject(),
            sap_projects.NPr4StudentAssignmentProject(),
            sap_projects.NPr5StudentAssignmentProject(),
            sap_projects.NPr6StudentAssignmentProject(),
            sap_projects.NPr7StudentAssignmentProject(),
            sap_projects.NPr8StudentAssignmentProject(),
            sap_projects.NPr9StudentAssignmentProject(),
            sap_projects.NPr10StudentAssignmentProject(),
        ]
        super().__init__(projects)


class FibonacciStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.Fibonacci1StudentAssignmentProject(),
            sap_projects.Fibonacci2StudentAssignmentProject(),
            sap_projects.Fibonacci3StudentAssignmentProject(),
            sap_projects.Fibonacci4StudentAssignmentProject(),
            sap_projects.Fibonacci5StudentAssignmentProject(),
            sap_projects.Fibonacci6StudentAssignmentProject(),
            sap_projects.Fibonacci7StudentAssignmentProject(),
            sap_projects.Fibonacci8StudentAssignmentProject(),
            sap_projects.Fibonacci9StudentAssignmentProject(),
            sap_projects.Fibonacci10StudentAssignmentProject(),
        ]
        super().__init__(projects)


class NumberOfDivisorsStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.NumberOfDivisors1StudentAssignmentProject(),
            sap_projects.NumberOfDivisors2StudentAssignmentProject(),
            sap_projects.NumberOfDivisors3StudentAssignmentProject(),
            sap_projects.NumberOfDivisors4StudentAssignmentProject(),
            sap_projects.NumberOfDivisors5StudentAssignmentProject(),
            sap_projects.NumberOfDivisors6StudentAssignmentProject(),
            sap_projects.NumberOfDivisors7StudentAssignmentProject(),
            sap_projects.NumberOfDivisors8StudentAssignmentProject(),
            sap_projects.NumberOfDivisors9StudentAssignmentProject(),
            sap_projects.NumberOfDivisors10StudentAssignmentProject(),
        ]
        super().__init__(projects)


class BubbleSortStudentAssignmentRepository(StudentAssignmentRepository):
    def __init__(self):
        projects: List[sap_projects.StudentAssignmentProject] = [
            sap_projects.BubbleSort1StudentAssignmentProject(),
            sap_projects.BubbleSort2StudentAssignmentProject(),
            sap_projects.BubbleSort3StudentAssignmentProject(),
            sap_projects.BubbleSort4StudentAssignmentProject(),
            sap_projects.BubbleSort5StudentAssignmentProject(),
            sap_projects.BubbleSort6StudentAssignmentProject(),
            sap_projects.BubbleSort7StudentAssignmentProject(),
            sap_projects.BubbleSort8StudentAssignmentProject(),
            sap_projects.BubbleSort9StudentAssignmentProject(),
            sap_projects.BubbleSort10StudentAssignmentProject(),
        ]
        super().__init__(projects)
