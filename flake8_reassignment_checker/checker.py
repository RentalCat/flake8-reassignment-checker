import ast
from typing import Iterator, Tuple

from . import __version__ as version


class ReassignmentChecker:
    name = "reassignment-checker"
    version = version

    def __init__(self, tree: ast.Module, filename: str) -> None:
        self.tree = tree

    def run(self) -> Iterator[Tuple[int, int, str, type]]:
        if False:
            yield 0, 0, "ERROR", type(self)
