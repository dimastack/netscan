# Makefile for netscan backend

VENV_NAME=venv

# venv commands
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

# Alembic migration commands
alembic-init:
	alembic init migrations

alembic-revision:
	alembic revision --autogenerate -m "$(msg)"

alembic-upgrade:
	alembic upgrade head

alembic-downgrade:
	alembic downgrade -1

alembic-current:
	alembic current

alembic-history:
	alembic history --verbose

alembic-show:
	alembic show $(rev)

alembic-merge:
	alembic merge -m "$(msg)" $(revisions)

alembic-heads:
	alembic heads
