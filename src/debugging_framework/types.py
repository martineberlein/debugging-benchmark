from typing import Callable, Union, Sequence, Type, Dict, List, Tuple, Any
from debugging_framework.input import Input
import re
#Harness Function for BenchmarkRepositorys
HARNESS_FUNCTION = Type[Callable[[Union[str, Input]], Sequence[str]]]

#Wieso Option kann man nicht von typing Optional verwenden? mhh eig nicht
Option = Dict[str, Any]
Expansion = Union[str, Tuple[str, Option]]

#Grammars
Grammar = Dict[str, List[Expansion]]
START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')