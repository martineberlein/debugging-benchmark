import unittest

from debugging_framework.coverage import population_coverage, population_branch_coverage
from .resources.program_simple_coverage import program_simple


@unittest.skip
class TestCoverage(unittest.TestCase):
    def test_coverage(self):
        all_coverage, cumulative = population_coverage(["sqrt(10)"], program_simple)

        self.assertEqual(cumulative, [2])
        # lines of the program should not change!
        self.assertEqual(all_coverage, {("program_simple", 2), ("program_simple", 3)})

    def test_coverage_population(self):
        all_coverage, cumulative = population_coverage(
            ["sqrt(10)", "tan(1)"], program_simple
        )

        self.assertEqual(cumulative, [2, 5])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                ("program_simple", 2),
                ("program_simple", 3),
                ("program_simple", 4),
                ("program_simple", 6),
                ("program_simple", 7),
            },
        )
        self.assertNotIn(("program_simple", 5), all_coverage)

    def test_branch_coverage(self):
        all_coverage, cumulative = population_branch_coverage(
            ["sqrt(10)"], program_simple
        )

        self.assertEqual(cumulative, [1])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                (("program_simple", 2), ("program_simple", 3)),
            },
        )
        self.assertNotIn((("program_simple", 2), ("program_simple", 4)), all_coverage)

    def test_branch_coverage_population(self):
        all_coverage, cumulative = population_branch_coverage(
            ["sqrt(10)", "tan(1)"], program_simple
        )

        self.assertEqual(cumulative, [1, 4])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                (("program_simple", 2), ("program_simple", 3)),
                (("program_simple", 2), ("program_simple", 4)),
                (("program_simple", 4), ("program_simple", 6)),
                (("program_simple", 6), ("program_simple", 7)),
            },
        )
        self.assertNotIn((("program_simple", 4), ("program_simple", 5)), all_coverage)


if __name__ == "__main__":
    unittest.main()
