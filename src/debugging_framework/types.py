from typing import Callable, Union, Sequence, Type, Dict, List, Tuple, Any
from debugging_framework.input import Input

HARNESS_FUNCTION = Type[Callable[[Union[str, Input]], Sequence[str]]]

Option = Dict[str, Any]
Expansion = Union[str, Tuple[str, Option]]
Grammar = Dict[str, List[Expansion]]
