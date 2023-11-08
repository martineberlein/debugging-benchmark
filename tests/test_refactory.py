import unittest

from debugging_benchmark.refactory import *


def check_directory_exists(path):
    return os.path.isdir(path)


class TestRefactory(unittest.TestCase):

    def test_question1_refactory_benchmark_repository(self):
        repo = Question1RefactoryBenchmarkRepository()
        self.assertEqual(repo.name,"RefactoryQ1")
        self.assertTrue(check_directory_exists(repo.get_dir()))

    def test_question1_build_test_programs(self):
        repo = Question1RefactoryBenchmarkRepository()
        test_subjects = repo.build()

        for test_subject in test_subjects:
            self.assertTrue(isinstance(test_subject, RefactoryBenchmarkProgram))


if __name__ == '__main__':
    unittest.main()
