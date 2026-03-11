.PHONY: run test lint setup

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt && pip install pytest

run:
	. venv/bin/activate && python app.py

test:
	. venv/bin/activate && python -m pytest tests/ -v

lint:
	. venv/bin/activate && python -m py_compile app.py && python -m py_compile tournament.py
