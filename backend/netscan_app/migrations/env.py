import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Import your models and Base
from netscan_app.core.config import Config
from netscan_app.models import Base  # <-- this imports all via __init__.py

# Load Alembic .ini
config = context.config
fileConfig(config.config_file_name)

# Inject DB URI dynamically
config.set_main_option("sqlalchemy.url", Config.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    url = Config.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
