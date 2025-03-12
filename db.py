import psycopg2
import os


def main():
    # Connection string
    conn_str = os.getenv("PSQL_CONN_STR")
    if not conn_str:
        raise ValueError(
            "No connection string found in environment variable 'PSQL_CONN_STR'"
        )
    try:
        # Create a new database session
        conn = psycopg2.connect(conn_str)
    except Exception as e:
        print(f"Unable to connect to the database: {e}")

    try:
        # Create a new cursor object.
        cur = conn.cursor()
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS moovies;
        """)

        # Test Query
        cur.execute("""
            CREATE TABLE IF NOT EXISTS "moovies"."posts" (
                    id          SERIAL PRIMARY KEY,
                    status      VARCHAR(50) NOT NULL,
                    author_id   INTEGER NOT NULL,
                    content     JSON,
                    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close communication with the database
        conn.commit()
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
