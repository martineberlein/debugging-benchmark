import unittest
from debugging_benchmark.database import DatabaseHelper
from debugging_benchmark.student_assignments import GCDStudentAssignmentBenchmarkRepository
from debugging_benchmark.refactory import Question1RefactoryBenchmarkRepository

class TestStudentAssignments(unittest.TestCase):
    def setUp(self):
        self._instance = DatabaseHelper.instance()

    def test_instance(self):
        self.assertIsInstance(self._instance, DatabaseHelper)

    def test_insert_program(self):
        repo = GCDStudentAssignmentBenchmarkRepository()
        programs = repo.build()
        print(len(programs))
        for program in programs:
            print(self._instance.insert_program(program))
        #bekomme ich jedesmal wenn ich den test ausführe einen neuen eintrag in die db? also müsste erst 1 dann 2



if __name__ == "__main__":
    unittest.main()