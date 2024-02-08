from enum import Enum


class OracleResult(Enum):
    FAILING = "FAILING"
    PASSING = "PASSING"
    UNDEFINED = "UNDEFINED"

    def __str__(self):
        """Returns the string representation of the enum value."""
        return self.value

    def to_bool(self):
        """
        Returns True if the result indicates a failing condition, False otherwise.

        The method considers only 'FAILING' as indicating a failure, with both
        'PASSING' and 'UNDEFINED' considered as not indicating failure.
        """
        return self == OracleResult.FAILING
