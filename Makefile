VENV_NAME = venv
VENV_PATH = $(VENV_NAME)/bin/activate
SRC_DIR = src
PYTHON := venv/bin/python

.PHONY: venv

venv:
ifeq ($(OS),Windows_NT)
	python -m venv $(VENV_NAME)
	. $(VENV_PATH) && pip install -r requirements.txt
else
	python3 -m venv $(VENV_NAME)
	. $(VENV_PATH); pip install -r requirements.txt
endif

.PHONY: test

test:
	@export FLASK_ENV=test && python -m pytest tests/

.PHONY: install

install: venv
	. $(VENV_PATH); pip install --upgrade -r requirements.txt

.PHONY: install-dev

install-dev: venv
	. $(VENV_PATH); pip install --upgrade -r requirements-dev.txt

.PHONY: update

update: venv
	. $(VENV_PATH); pip install --upgrade -r requirements.txt

.PHONY: clean

clean:
	rm -rf $(VENV_NAME)

check-autopep:
	${PYTHON} -m autopep8 $(SRC_DIR)/*.py tests/*.py --in-place

check-isort:
	${PYTHON} -m isort --check-only $(SRC_DIR)  tests

check-flake:
	${PYTHON} -m flake8 $(SRC_DIR)  tests

check-mypy:
	${PYTHON} -m mypy --strict --implicit-reexport $(SRC_DIR) 

lint: check-flake check-mypy check-autopep check-isort

format:
	. $(VENV_PATH);
	${PYTHON} -m autopep8 $(SRC_DIR)/*.py tests/*.py --in-place
	${PYTHON} -m isort $(SRC_DIR) tests

guni:
	gunicorn -w 4 -b 0.0.0.0:5000 app:app
