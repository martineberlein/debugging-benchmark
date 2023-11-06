import unittest

from debugging_benchmark.student_assignments import MPITestSubjectFactory, EratosthenesTestSubject


class TestStudentAssignments(unittest.TestCase):
    def test_build_sieveOfEratosthenes(self):

        subjects = MPITestSubjectFactory([EratosthenesTestSubject]).build()
        for subject in subjects:
            print(f"Subject {subject.id}")
            param = subject.to_dict()
            oracle = param.get("oracle")
            for inp in param.get("initial_inputs"):
                print(inp, oracle(inp))


if __name__ == '__main__':
    unittest.main()
