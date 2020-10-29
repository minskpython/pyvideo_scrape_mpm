test:
	PYTHONPATH=. coverage run -m unittest discover -s test
	coverage report -m
	flake8
