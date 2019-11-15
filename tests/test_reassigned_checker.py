from conftest import run_validator_for_test_file


def test_success() -> None:
    errors = run_validator_for_test_file("success.py")
    assert len(errors) == 0
