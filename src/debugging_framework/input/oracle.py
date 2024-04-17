from enum import Enum


class OracleResult(Enum):
    """
    An enumeration representing possible results of an oracle's evaluation of test inputs.

    This enum defines three states:
    - FAILING: Represents a condition where the test input causes the system under test to fail.
    - PASSING: Represents a condition where the test input does not cause any failure.
    - UNDEFINED: Represents a condition where the outcome is inconclusive or not defined.
    """

    FAILING = "FAILING"
    PASSING = "PASSING"
    UNDEFINED = "UNDEFINED"

    def __str__(self) -> str:
        """
        Returns the string representation of the oracle result.
        :return str: The string representation of the enum value.
        """
        return self.value

    def is_failing(self) -> bool:
        """
        Determines whether the oracle result indicates a failing condition.
        :return bool: True if the result is 'FAILING', otherwise False.
        """
        return self == OracleResult.FAILING
