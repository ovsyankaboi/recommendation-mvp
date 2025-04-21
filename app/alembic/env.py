from logging.config import fileConfig
import os, sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Добавляем корневую папку app/ в путь для импорта моделей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

# (Опционально) загрузка .env
from dotenv import load_dotenv
load_dotenv()

# Импортируем metadata вашей модели
import models
target_metadata = models.Base.metadata

# Подгружаем конфиг
config = context.config
# Если хотите брать URL из .env:
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', config.get_main_option('sqlalchemy.url')))
fileConfig(config.config_file_name)

from sqlalchemy import engine_from_config, pool
from alembic import context

# 👇 добавлено
from dotenv import load_dotenv
import os
load_dotenv()

from app import models  # 👈 добавлено подключение твоих моделей

# Получаем настройки Alembic
config = context.config

# Настройка логгера
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👇 Здесь указываем метаданные твоих моделей
target_metadata = models.Base.metadata

# URL подключения к базе данных из переменных окружения
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
