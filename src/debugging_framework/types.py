from typing import Callable, Union, Sequence, Type
from debugging_framework.input import Input

HARNESS_FUNCTION = Type[Callable[[Union[str, Input]], Sequence[str]]]
