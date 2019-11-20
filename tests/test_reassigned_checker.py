from conftest import run_validator_for_test_file


def test_success() -> None:
    assert run_validator_for_test_file("success.py") == []


def test_failure() -> None:
    assert run_validator_for_test_file("failure.py") == [
        (2, -1, 'RAC001 variable "hoge" (defined in line 1) has been reassigned.'),
    ]
