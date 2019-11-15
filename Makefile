check:
	flake8 .
	mypy --strict .
	python -m pytest --cov=flake8_reassignment_checker --cov-report=xml
