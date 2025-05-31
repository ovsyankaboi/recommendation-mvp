from logging.config import fileConfig
import os, sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))
from dotenv import load_dotenv
load_dotenv()
import models
target_metadata = models.Base.metadata
config = context.config
# Если хотите брать URL из .env:
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', config.get_main_option('sqlalchemy.url')))
fileConfig(config.config_file_name)

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
import os
load_dotenv()

from app import models
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = models.Base.metadata
DATABASE_URL = os.getenv('DATABASE_URL')

def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,  # 👈 используем DATABASE_URL из .env
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = DATABASE_URL  # 👈 используем DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
