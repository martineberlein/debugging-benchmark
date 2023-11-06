from enum import Enum


class OracleResult(Enum):
    FAILING = "FAILING"
    PASSING = "PASSING"
    UNDEFINED = "UNDEFINED"

    def __str__(self):
        return self.value
