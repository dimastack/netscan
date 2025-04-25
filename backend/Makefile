# Makefile for netscan backend

VENV_NAME=venv

venv:
	python3 -m venv $(VENV_NAME)

install:
	source $(VENV_NAME)/bin/activate && pip install -r requirements.txt

freeze:
	source $(VENV_NAME)/bin/activate && pip freeze > requirements.txt

run:
	source $(VENV_NAME)/bin/activate && python app/main.py

clean:
	rm -rf $(VENV_NAME)
