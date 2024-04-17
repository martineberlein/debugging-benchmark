from typing import Callable, Sequence, Type, Dict, List, Tuple, Any, Optional, Union, Set
from debugging_framework.input.input import Input
import re
from debugging_framework.input.oracle import OracleResult

# Harness Function for BenchmarkRepositorys
HARNESS_FUNCTION = Type[Callable[[Union[str, Input]], Sequence[str]]]

Option = Dict[str, Any]
Expansion = Union[str, Tuple[str, Option]]

# Grammars
Grammar = Dict[str, List[Expansion]]
START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r"(<[^<> ]*>)")

OracleResultType = Tuple[OracleResult, Optional[Exception]]
OracleType = Callable[[Union[Input, str]], OracleResultType]
BatchOracleType = Callable[[Union[Set[Input], Set[str]]], List[OracleResultType]]
