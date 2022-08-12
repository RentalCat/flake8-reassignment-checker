from __future__ import annotations

import ast
import os

from flake8_reassignment_checker.checker import ReassignmentChecker

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


def run_validator_for_test_file(filename: str) -> list[tuple[int, int, str, type]]:
    with open(os.path.join(TEST_FILES_DIR, filename)) as f:
        lines = f.read()
        return list(ReassignmentChecker(ast.parse(lines), filename, lines).run())
