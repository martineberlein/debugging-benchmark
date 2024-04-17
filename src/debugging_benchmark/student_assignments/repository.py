from typing import List, Dict, Sequence, Any, Callable, Type
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import string

from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_framework.input.oracle import OracleResult
from debugging_benchmark.student_assignments.program import StudentAssignmentBenchmarkProgram


class StudentAssignmentRepository(BenchmarkRepository, ABC):
    programs: List[Type[StudentAssignmentBenchmarkProgram]]

    @abstractmethod
    def harness_function(self, input_str: str) -> Sequence[Any]:
        pass

    def get_dir(self) -> str:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(Path(repo_dir), Path("student_assignments"))

    def get_ground_truth_location(self) -> str:
        return os.path.join(self.get_dir(), Path("reference1.py"))

    def load_ground_truth(self):
        path_to_ground_truth = self.get_ground_truth_location()
        return load_function_from_class(
            path_to_ground_truth, self.get_implementation_function_name()
        )

    def load_implementation(self, bug_id) -> Callable:
        path_to_implementation = os.path.join(
            self.get_dir(), Path(f"prog_{bug_id}/buggy.py")
        )

        return load_function_from_class(
            path_to_implementation, self.get_implementation_function_name()
        )

    def _construct_test_program(
        self,
        bug_id: int,
        benchmark_program: Type[StudentAssignmentBenchmarkProgram],
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> StudentAssignmentBenchmarkProgram:
        ground_truth = self.load_ground_truth()
        program = self.load_implementation(bug_id)

        oracle = construct_oracle(
            program_under_test=program,
            program_oracle=ground_truth,
            error_definitions=err_def,
            default_oracle_result=default_oracle,
            timeout=0.01,
            harness_function=self.harness_function,
        )

        return benchmark_program(
            name=self.get_name(),
            bug_id=bug_id,
            grammar=self.get_grammar(),
            # initial_inputs=self.get_initial_inputs(),
            oracle=oracle,
        )

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[StudentAssignmentBenchmarkProgram]:
        constructed_test_programs: List[StudentAssignmentBenchmarkProgram] = []
        for bug_id, program in enumerate(self.programs):
            try:
                subject = self._construct_test_program(
                    bug_id=bug_id + 1,
                    benchmark_program=program,
                    err_def=err_def,
                    default_oracle=default_oracle,
                )
                constructed_test_programs.append(subject)

            except Exception as e:
                print(f"Subject {bug_id} could not be built.")
                print(e)

        return constructed_test_programs

    def get_all_test_programs(self) -> List[BenchmarkProgram]:
        pass