import os
import urllib.parse
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# 1. LOAD CONFIGURATION FROM .ENV
load_dotenv()

# Ambil kredensial database dari file .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Amankan password dari spesial karakter (seperti % ke %25)
safe_password = urllib.parse.quote_plus(db_password)

# Susun URL Koneksi PostgreSQL
raw_url = f"postgresql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}"

# Trik khusus agar library configparser milik Alembic tidak crash membaca karakter '%'
escaped_url = raw_url.replace('%', '%%')

# 2. ALEMBIC CONFIG OBJECT
config = context.config

# Setel URL yang sudah aman ke dalam konfigurasi utama Alembic
config.set_main_option("sqlalchemy.url", escaped_url)

# Interpretasikan file config untuk logging bawaan
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. IMPORT TARGET METADATA FROM YOUR MODEL
# Import 'Base' dari file day4.py lu agar Alembic tahu struktur tabelnya
from day4 import Base
target_metadata = Base.metadata

# 4. RUN MIGRATIONS FUNCTIONS
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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