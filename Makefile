.PHONY: cleanup venv install freeze run clean \
        alembic-init alembic-revision alembic-upgrade alembic-downgrade \
        alembic-current alembic-history alembic-show alembic-merge alembic-heads

# Cleanup __pycache__ directories
cleanup:
	find . -type d -name "__pycache__" -exec rm -r {} +

# Delegate to backend Makefile
venv install freeze run clean \
alembic-init alembic-revision alembic-upgrade alembic-downgrade \
alembic-current alembic-history alembic-show alembic-merge alembic-heads:
	$(MAKE) -C backend $@
