import os
from pathlib import Path

import psycopg

database_url = os.environ["DATABASE_URL"]
migrations_dir = Path(__file__).parent / "migrations"

with psycopg.connect(database_url) as conn:
    for migration_file in sorted(migrations_dir.glob("*.sql")):
        print(f"Applying migration: {migration_file.name}")
        conn.execute(migration_file.read_text(encoding="utf-8"))

print("All migrations applied successfully.")