

from contextlib import closing

from psycopg2.extras import DictCursor

from database import postgres_connection


def main():
    with closing(postgres_connection()) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("select count(1) as users from public.user")
            row = cur.fetchone()

    print(f"Количество пользователей: {row['users']}")


if __name__ == "__main__":
    main()
