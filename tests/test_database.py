import unittest
from debugging_benchmark.database import DatabaseHelper
from debugging_benchmark.student_assignments import GCDStudentAssignmentBenchmarkRepository

from debugging_framework.oracle import OracleResult

class TestStudentAssignments(unittest.TestCase):
    def setUp(self):
        self._instance = DatabaseHelper.instance()
        repo = GCDStudentAssignmentBenchmarkRepository()
        self._programs = repo.build()

    def test_1_instance(self):
        self.assertIsInstance(self._instance, DatabaseHelper)

    def test_2_insert_program(self):
        #TODO: die einträge suchen und ein assert
        for program in self._programs:
            self._instance.insert_program(program)

    def test_3_get_program_id(self):
        for program in self._programs:
            print(self._instance.get_program_id(program))

    def test_4_insert_failing_input(self):
        test_input = "test"
        for program in self._programs:
            program_id = self._instance.insert_program(program)
            self._instance.insert_failing_input(program_id, test_input+program.get_name())
    
    def test_5_insert_passing_input(self):
        test_input = "test"
        for program in self._programs:
            program_id = self._instance.insert_program(program)
            self._instance.insert_passing_input(program_id, test_input+program.get_name())
    
    def test_6_get_inputs(self):
        for program in self._programs:
            print(self._instance.get_inputs_from_program(program))

    def test_7_delete_program(self):     
        for program in self._programs:
            self._instance.delete_program(program)

    def test_8_get_count_inputs(self):
        program = self._programs[0]
        program_id = self._instance.insert_program(program)
        test_input = "test"
        self._instance.insert_passing_input(program_id, test_input+"1")
        self._instance.insert_passing_input(program_id, test_input+"2")
        self._instance.insert_failing_input(program_id, test_input+"3")
        counts = self._instance.get_count_inputs(program_id)
        print(counts)

    def test_9_insert_input(self):
        self._instance.insert_input(12, "test12", OracleResult.PASSING)

if __name__ == "__main__":
    unittest.main()