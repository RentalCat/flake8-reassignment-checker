from __future__ import annotations

import glob
import ast
import pytest
import typing as t
import os
import re

from itertools import dropwhile
from flake8_reassignment_checker import ReassignmentChecker

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


def _load_error_cases(lines: str) -> t.Iterator[str]:
    for line in dropwhile(lambda x: not re.match("ERRORS:", x), lines.split("\n")):
        m = re.match(r"    (:[\d+:[\d]+:.*)", line)
        if m:
            yield m.group(1)


def _run_checker(filepath: str, lines: str) -> t.Iterator[str]:
    tree: ast.Module = ast.parse(lines, filepath)
    for l_num, c_num, msg, _ in ReassignmentChecker(tree, filepath, lines).run():
        yield f":{l_num}:{c_num}:{msg}"


@pytest.mark.parametrize("filepath", glob.glob(os.path.join(TEST_FILES_DIR, "*.py")))
def test_success(filepath: str) -> None:
    with open(filepath) as f:
        lines: str = f.read()
    assert list(_run_checker(filepath, lines)) == list(_load_error_cases(lines))
