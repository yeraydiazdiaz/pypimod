.PHONY: pin-requirements install-dev tests

pin-requirements:
	pip-compile --build-isolation --output-file=requirements/main.txt requirements/main.in

install-dev:
	pip install -r requirements/dev.txt
	pip install -e .[tests]

tests:
	ENV_FILE=env/test.env pytest ${T}
