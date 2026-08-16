import os
import sys
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("ERROR: DATABASE_URL is not set.")
    print("Copy .env.example to .env and fill in your MySQL credentials.")
    sys.exit(1)

print(f"\nDatabase URL: {db_url[:db_url.index('@') + 1]}***")
print("-" * 60)

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import OperationalError

    engine = create_engine(db_url)

    with engine.connect() as conn:
        print("MySQL connection successful\n")

        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        print(f"Connected to database: {db_name}")

        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]

        required = {"users", "categories", "expenses"}
        found = required.intersection(set(tables))
        missing = required - set(tables)

        for t in sorted(found):
            print(f"Table found: {t}")

        if missing:
            print()
            for t in sorted(missing):
                print(f"Table MISSING: {t}")
            print("\nRun the Week 3 schema file first:")
            print("  mysql -u root -p < ../../week_3_db/expense_tracker_db/expense_tracker_schema.sql")
            sys.exit(1)

        print()

        for table in ["users", "categories", "expenses"]:
            result = conn.execute(text(f"SELECT COUNT(*) FROM `{table}`"))
            count = result.scalar()
            print(f"  {table}: {count} row(s)")

        print()
        print("=" * 60)
        print("Database is ready. You can now start the API:")
        print("   uvicorn main:app --reload")
        print("=" * 60)
        print()

except OperationalError as e:
    print(f"\nCould not connect to MySQL: {e}")
    sys.exit(1)

except Exception as e:
    print(f"\nUnexpected error: {e}")
    sys.exit(1)
