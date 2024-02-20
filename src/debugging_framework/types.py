from typing import Callable, Union, Sequence, Type, Dict, List, Tuple, Any, Optional
from debugging_framework.input import Input
import re

#Harness Function for BenchmarkRepositorys
HARNESS_FUNCTION = Type[Callable[[Union[str, Input]], Sequence[str]]]

Option = Dict[str, Any]
Expansion = Union[str, Tuple[str, Option]]
DerivationTree = Tuple[str, Optional[List[Any]]]

#Grammars
Grammar = Dict[str, List[Expansion]]
START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')