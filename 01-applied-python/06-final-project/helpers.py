

from typing import List, Optional
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from models import User, Post, Feed


def get_user(conn: connection, user_id: int) -> Optional[User]:


    query = """
        SELECT *
        FROM public."user"
        WHERE id = %s
    """

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (user_id,))
        row = cur.fetchone()

        return User(**row) if row else None


def get_post(conn: connection, post_id: int) -> Optional[Post]:


    query = """
        SELECT *
        FROM public.post
        WHERE id = %s
    """

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (post_id,))
        row = cur.fetchone()

        return Post(**row) if row else None


def get_feed(
    conn: connection, user_id: int = None, post_id: int = None, limit: int = 10
) -> List[Feed]:


    if user_id is None and post_id is None:
        raise ValueError("Необходимо указать хотя бы user_id или post_id")

    query = """
        SELECT f.user_id,f.post_id,f.action,f.time,u.gender,
        u.age,u.country,u.city,u.exp_group,u.os,u.source,
        p.text,p.topic

        FROM public.feed_action AS f
        
        JOIN public."user" AS u ON f.user_id = u.id
        JOIN public.post AS p ON f.post_id = p.id

        WHERE
            (%s IS NULL OR f.user_id = %s)
            AND (%s IS NULL OR f.post_id = %s)

        ORDER BY f.time DESC
        LIMIT %s
    """

    result = []

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(
            query,
            (user_id, user_id, post_id, post_id, limit)
        )

        rows = cur.fetchall()

        for row in rows:
            user = User(
                id=row["user_id"],
                gender=row["gender"],
                age=row["age"],
                country=row["country"],
                city=row["city"],
                exp_group=row["exp_group"],
                os=row["os"],
                source=row["source"],
            )

            post = Post(
                id=row["post_id"],
                text=row["text"],
                topic=row["topic"],
            )

            feed = Feed(
                user_id=row["user_id"],
                post_id=row["post_id"],
                user=user,
                post=post,
                action=row["action"],
                time=row["time"],
            )

            result.append(feed)

    return result


def get_recommended_feed(conn: connection, id: int, limit: int) -> List[Post]:


    query = """
        SELECT
            p.id,
            p.text,
            p.topic

        FROM public.post AS p

        JOIN public.feed_action AS f
            ON p.id = f.post_id

        WHERE f.action = 'like'

        GROUP BY
            p.id,
            p.text,
            p.topic

        ORDER BY COUNT(*) DESC

        LIMIT %s
    """

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (limit,))
        rows = cur.fetchall()

        return [Post(**row) for row in rows]
