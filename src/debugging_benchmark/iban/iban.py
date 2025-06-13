import math
from typing import Union, Callable, List, Dict, Tuple
import string

from debugging_framework.input.input import Input
from debugging_framework.types import Grammar
from debugging_framework.input.oracle import OracleResult
from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository


def validate_iban(iban: str) -> bool:
    """
    Very simple IBAN validity check:
      - No per-country length verification.
    """
    rotated = iban[4:] + iban[:4]
    num_str = "".join(str(int(ch, 36)) for ch in rotated)
    try:
        return int(num_str) % 97 == 1
    except ValueError:
        return False


def oracle(iban: str | Input) -> Tuple[OracleResult, Union[Exception, None]]:
    """
    Oracle function to validate IBANs.
    """
    return (OracleResult.FAILING, None) if validate_iban(str(iban)) else (OracleResult.PASSING, None)


grammar = {
    "<start>": ["<iban>"],
    "<iban>": [
        "<country_code><checksum><bban>",
    ],
    "<country_code>": ["DE", "AT", "CH", "ES", "FR", "IT", "NL", "BE", "LU", "GB"],
    "<checksum>": ["<digit><digit>"],
    "<bban>": ["<number>"],
    "<number>": ["<digit><number>", "<digit>"],
    "<digit>": [str(num) for num in range(10)],
}



class IBANBenchmarkRepository(BenchmarkRepository):
    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[BenchmarkProgram]:
        return [
            BenchmarkProgram(
                name="calculator",
                grammar=grammar,
                oracle=oracle,
                failing_inputs=["IT3405012","DE02600501010002034304","GB824474", "DE02701500000000594937", "FR432243", "DE02120300000000202051", "AT611904300234573201", "CH9300762011623852957"],
                passing_inputs=["GB7163820", "CH4844", "GB392980", "IT914775", "NL68847"],
            )
        ]
