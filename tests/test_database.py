import unittest
from debugging_benchmark.database import DatabaseHelper
from debugging_benchmark.student_assignments import GCDStudentAssignmentBenchmarkRepository
from debugging_benchmark.refactory import Question1RefactoryBenchmarkRepository

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
        


if __name__ == "__main__":
    unittest.main()