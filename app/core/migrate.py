from sqlalchemy import text
from sqlalchemy.engine import Engine

# Migration minimale, le temps d'introduire un vrai outil (Alembic) au projet.
# Chaque instruction est idempotente (ADD COLUMN IF NOT EXISTS).
_STATEMENTS = [
    "ALTER TABLE utilisateurs ADD COLUMN IF NOT EXISTS actif BOOLEAN NOT NULL DEFAULT TRUE",
    "ALTER TABLE utilisateurs ADD COLUMN IF NOT EXISTS reset_token VARCHAR",
    "ALTER TABLE utilisateurs ADD COLUMN IF NOT EXISTS reset_token_expire TIMESTAMPTZ",
    "ALTER TABLE patients ADD COLUMN IF NOT EXISTS fichier_joint VARCHAR",
    "ALTER TABLE patients ADD COLUMN IF NOT EXISTS adresse VARCHAR",
    "ALTER TABLE patients ADD COLUMN IF NOT EXISTS telephone VARCHAR",
]


def appliquer_migrations(engine: Engine) -> None:
    with engine.begin() as conn:
        for statement in _STATEMENTS:
            conn.execute(text(statement))
