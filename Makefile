check:
	flake8 .
	mypy --strict .
	black --check .
	python -m pytest --cov=flake8_reassignment_checker --cov-report=xml
	xenon -max-absolute B --max-modules A --max-average A
