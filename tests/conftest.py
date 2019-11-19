import ast
import os
from typing import List, Tuple

from flake8_reassignment_checker.checker import ReassignmentChecker


def run_validator_for_test_file(filename: str,) -> List[Tuple[int, int, str]]:
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_files", filename,
    )
    with open(test_file_path, "r") as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = ReassignmentChecker(tree=tree, filename=filename)

    return [(lineno, col_offset, msg) for lineno, col_offset, msg, _ in checker.run()]
