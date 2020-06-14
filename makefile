.PHONY: pin-requirements install-dev tests lint

pin-requirements:
	pip-compile --build-isolation --output-file=requirements/main.txt requirements/main.in

install-dev:
	pip install -U pip wheel setuptools
	pip install -r requirements/dev.txt
	pip install -e .[tests]

tests:
	ENV_FILE=env/test.env pytest ${T}

lint:
	flake8 src tests
