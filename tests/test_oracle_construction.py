import unittest
import string

from debugging_framework.input.oracle_construction import (
    FailureOracleConstructor,
    FunctionalOracleConstructor,
    UnexpectedResultError,
)
from debugging_framework.input.oracle import OracleResult
from debugging_framework.input.input import Input
from debugging_framework.types import Grammar
from debugging_framework.execution.timeout_manager import ManageTimeout

grammar: Grammar = {
    "<start>": ["<input>"],
    "<input>": ["<first> <second>"],
    "<first>": ["<integer>"],
    "<second>": ["<integer>"],
    "<integer>": ["<one_nine><maybe_digits>"],  # no 0 at the moment
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


class TestConstructOracle(unittest.TestCase):
    def setUp(self):
        self.error_definitions = {
            UnexpectedResultError: OracleResult.FAILING,
            TimeoutError: OracleResult.UNDEFINED,
        }
        self.harness_function = lambda inp: list(map(int, str(inp).strip().split()))

    def test_same_result(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            return x + y

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions=self.error_definitions,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.PASSING)

    def test_different_result(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            return x - y

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions=self.error_definitions,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_defined_exception(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise TimeoutError()

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions=self.error_definitions,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.UNDEFINED)

    def test_undefined_exception(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise ValueError()

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions=self.error_definitions,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.UNDEFINED)

    def test_timeout_sleep(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions={TimeoutError: OracleResult.FAILING},
            timeout=1,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_no_error_definition(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise ValueError

        def under_test_unexpected_result_error(x, y):
            raise x + y + 1

        def under_test_timeout(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

        my_oracle = FunctionalOracleConstructor(
            under_test_unexpected_result_error,
            oracle,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

        my_oracle = FunctionalOracleConstructor(
            under_test_timeout,
            oracle,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_timeout_sleep_fraction(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = FunctionalOracleConstructor(
            under_test,
            oracle,
            error_definitions={TimeoutError: OracleResult.FAILING},
            timeout=0.5,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_failure_oracle(self):
        def under_test(x, y):
            return x + y

        my_oracle = FailureOracleConstructor(
            program=under_test,
            harness_function=self.harness_function
        ).build()

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertTrue(isinstance(oracle_result, OracleResult))

    @unittest.skip
    def test_oracle_sigkill(self):
        """
        Raises SIGKILL due to excessive Memory Consumption
        Needs to be fixed
        :return:
        """
        from debugging_benchmark.student_assignments.student_assignments import \
            SieveOfEratosthenesStudentAssignmentBenchmarkRepository

        SieveOfEratosthenesStudentAssignmentBenchmarkRepository().load_ground_truth()(
            4713133176770
        )

    @unittest.skip
    def test_timeout_manager(self):
        """
        Raises SIGKILL due to excessive Memory Consumption
        Needs to be fixed
        :return:
        """

        def sieveOfEratosthenes(N):
            is_prime = [True] * (N + 1)
            for i in range(2, N):
                if is_prime[i]:
                    for j in range(i * i, N + 1, i):
                        is_prime[j] = False

            # Get the list of primes
            result = []
            for i in range(2, N + 1):
                if is_prime[i]:
                    result.append(i)
            return result

        with ManageTimeout(1):
            print(sieveOfEratosthenes(4713133176770))

    def test_fix(self):
        """
        Possible Fix?
        :return:
        """

        def sieveOfEratosthenes(N):
            # Create the sieve
            is_prime = [True] * (N + 1)
            for i in range(2, N):
                if is_prime[i]:
                    for j in range(i * i, N + 1, i):
                        is_prime[j] = False

            # Get the list of primes
            result = []
            for i in range(2, N + 1):
                if is_prime[i]:
                    result.append(i)
            return result

        from concurrent.futures import (
            ProcessPoolExecutor,
            TimeoutError as FuturesTimeoutError,
        )

        # Use ProcessPoolExecutor to apply timeout to a function call
        with ProcessPoolExecutor() as executor:
            future = executor.submit(sieveOfEratosthenes, 4713133176770)
            try:
                result = future.result(timeout=1)  # Timeout after 1 second
                print(result)
            except FuturesTimeoutError:
                print("Function call timed out")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    unittest.main()
