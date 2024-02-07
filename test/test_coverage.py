import unittest

from debugging_framework.coverage import population_coverage, population_branch_coverage


# Program should not be moved, as this affects the executed lines of codes;
# moving might resolve in failing tests
def program_simple(inp: str) -> int:
    if inp.startswith("sqrt"):
        return 1
    elif inp.startswith("cos"):
        return 2
    elif inp.startswith("tan"):
        return 3


class TestCoverage(unittest.TestCase):
    def test_coverage(self):
        all_coverage, cumulative = population_coverage(["sqrt(10)"], program_simple)

        self.assertEqual(cumulative, [2])
        # lines of the program should not change!
        self.assertEqual(all_coverage, {("program_simple", 9), ("program_simple", 10)})

    def test_coverage_population(self):
        all_coverage, cumulative = population_coverage(
            ["sqrt(10)", "tan(1)"], program_simple
        )

        self.assertEqual(cumulative, [2, 5])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                ("program_simple", 9),
                ("program_simple", 10),
                ("program_simple", 11),
                ("program_simple", 13),
                ("program_simple", 14),
            },
        )
        self.assertNotIn(("program_simple", 12), all_coverage)

    def test_branch_coverage(self):
        all_coverage, cumulative = population_branch_coverage(
            ["sqrt(10)"], program_simple
        )

        self.assertEqual(cumulative, [1])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                (("program_simple", 9), ("program_simple", 10)),
            },
        )
        self.assertNotIn((("program_simple", 9), ("program_simple", 11)), all_coverage)

    def test_branch_coverage_population(self):
        all_coverage, cumulative = population_branch_coverage(
            ["sqrt(10)", "tan(1)"], program_simple
        )

        self.assertEqual(cumulative, [1, 4])
        # lines of the program should not be changed!
        self.assertEqual(
            all_coverage,
            {
                (("program_simple", 9), ("program_simple", 10)),
                (("program_simple", 9), ("program_simple", 11)),
                (("program_simple", 11), ("program_simple", 13)),
                (("program_simple", 13), ("program_simple", 14)),
            },
        )
        self.assertNotIn((("program_simple", 11), ("program_simple", 12)), all_coverage)


if __name__ == "__main__":
    unittest.main()
