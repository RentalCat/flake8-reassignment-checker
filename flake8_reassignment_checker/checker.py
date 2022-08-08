from __future__ import annotations

import ast
import typing as t

from . import __version__ as version


class ReassignmentChecker:
    name = "reassignment-checker"
    version = version

    def __init__(self, tree: ast.Module, filepath: str, lines: str) -> None:
        self.tree = tree

    def run(self) -> t.Iterator[tuple[int, int, str, type]]:
        if False:
            yield 0, 0, "ERROR", type(self)
