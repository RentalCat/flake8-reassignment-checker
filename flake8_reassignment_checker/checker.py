from __future__ import annotations

import ast
import typing as t


class ReassignmentChecker:
    name = "reassignment-checker"
    version = "0.0.1"

    def __init__(self, tree: ast.Module, filepath: str, lines: str) -> None:
        self.tree = tree

    def run(self) -> t.Iterator[tuple[int, int, str, type]]:
        if False:
            yield 0, 0, "ERROR", type(self)
