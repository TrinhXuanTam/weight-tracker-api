from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from src.config import db_config
from src.utils.db_utils import Base

# This is the Alembic Config object, which provides access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support.
# target_metadata allows Alembic to detect changes in models and apply the migration.
# Example:
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# Other values from the config, defined by the needs of `env.py`, can be acquired:
# Example:
# my_important_option = config.get_main_option("my_important_option")
DATABASE_URL = str(db_config.DATABASE_URL)

# Extract and adjust the database driver to use the synchronous version if necessary.
db_driver = db_config.DATABASE_URL.scheme
db_driver_parts = db_driver.split("+")
if len(db_driver_parts) > 1:  # e.g., postgresql+asyncpg
    sync_scheme = db_driver_parts[0].strip()
    DATABASE_URL = DATABASE_URL.replace(db_driver, sync_scheme)  # Replace with sync driver.

# Update the main SQLAlchemy URL in the Alembic configuration.
config.set_main_option("sqlalchemy.url", DATABASE_URL)
config.compare_type = True
config.compare_server_default = True


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.
    By skipping Engine creation, we don't need a DBAPI to be available.

    Calls to `context.execute` emit the given string to the migration script output.

    :return: None
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario, we need to create an Engine and associate a connection with the context.

    :return: None
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Determine whether to run migrations in offline or online mode based on the context.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
