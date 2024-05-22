from typing import Generator, Optional, Final

from isla.derivation_tree import DerivationTree
from isla.parser import EarleyParser

from debugging_framework.input.oracle import OracleResult


class Input:
    """
    Represents a test input comprising a derivation tree and an associated oracle result.
    The derivation tree represents the parsed structure of the input, and the oracle result
    provides the outcome when this input is processed by a system under test.
    """

    def __init__(self, tree: DerivationTree, oracle: OracleResult = None):
        """
        Initializes the Input instance with a derivation tree and an optional oracle result.

        :param DerivationTree tree: The derivation tree of the input.
        :param OracleResult oracle: The optional oracle result associated with the input.
        """
        assert isinstance(
            tree, DerivationTree
        ), "tree must be an instance of DerivationTree"
        self.__tree: Final[DerivationTree] = tree
        self.__oracle: Optional[OracleResult] = oracle

    @property
    def tree(self) -> DerivationTree:
        """
        Retrieves the derivation tree of the input.
        :return DerivationTree: The derivation tree.
        """
        return self.__tree

    @property
    def oracle(self) -> OracleResult:
        """
        Retrieves the oracle result associated with the input.
        :return OracleResult: The oracle result, or None if not set.
        """
        return self.__oracle

    @oracle.setter
    def oracle(self, oracle_: OracleResult):
        """
        Sets the oracle result for the input.
        :param OracleResult oracle_: The new oracle result to set.
        """
        self.__oracle = oracle_

    def update_oracle(self, oracle_: OracleResult) -> "Input":
        """
        Updates the oracle result for the input and returns the modified input instance.
        :param OracleResult oracle_: The new oracle result to set.
        :return Input: The current input instance with the updated oracle.
        """
        self.__oracle = oracle_
        return self

    def __repr__(self) -> str:
        """
        Provides the canonical string representation of the Input instance.
        :return str: A string representation that can recreate the Input instance.
        """
        return f"Input({repr(self.tree)}, {repr(self.oracle)})"

    def __str__(self) -> str:
        """
        Provides a user-friendly string representation of the Input's derivation tree.
        :return str: The string representation of the derivation tree.
        """
        return str(self.__tree)

    def __hash__(self) -> int:
        """
        Generates a hash based on the structural hash of the derivation tree.
        :return int: The hash value.
        """
        return self.__tree.structural_hash()

    def __eq__(self, other) -> bool:
        """
        Determines equality based on the structural hash of the derivation trees.
        :param other: The object to compare against.
        :return bool: True if the other object is an Input with an equal derivation tree.
        """
        return isinstance(other, Input) and self.__hash__() == hash(other)

    def __iter__(self) -> Generator[DerivationTree | OracleResult | None, None, None]:
        """
        Allows tuple unpacking of the input, e.g., tree, oracle = input.
        :return Generator[DerivationTree | OracleResult | None, None]: An iterator yielding the tree and oracle.
        """
        yield self.tree
        yield self.oracle

    def __getitem__(self, item: int) -> Optional[DerivationTree] | OracleResult:
        """
        Allows indexed access to the input's derivation tree and oracle.
        :param int item: The index of the item to get (0 for tree, 1 for oracle).
        :return Optional[DerivationTree] | OracleResult: The requested component of the input.
        """
        assert (
            isinstance(item, int) and 0 <= item <= 1
        ), "Index must be 0 (tree) or 1 (oracle)"
        return self.tree if item == 0 else self.oracle

    @classmethod
    def from_str(cls, grammar, input_string, oracle: Optional[OracleResult] = None):
        """
        Factory method to create an Input instance from a string using the specified grammar.
        :param grammar: The grammar used for parsing the input string.
        :param str input_string: The input string to parse.
        :param Optional[OracleResult] oracle: The optional oracle result.
        :return Input: The created Input instance.
        """
        return cls(
            DerivationTree.from_parse_tree(
                next(EarleyParser(grammar).parse(input_string))
            ),
            oracle,
        )
