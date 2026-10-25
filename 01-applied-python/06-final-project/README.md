# Feed API

A PostgreSQL-backed API returns users, posts and recent interactions. A simple
recommendation baseline returns posts ranked by total likes; it is identical for
all users and does not train an ML model.

| Endpoint | Behavior |
| --- | --- |
| `GET /user/{id}` | User attributes, or 404 |
| `GET /post/{id}` | Post text and topic, or 404 |
| `GET /user/{id}/feed?limit=10` | Recent user actions with nested user/post data, or 404 for an empty result |
| `GET /post/{id}/feed?limit=10` | Recent actions on a post, or 404 for an empty result |
| `GET /post/recommendations/?id=200&limit=10` | Posts ranked by likes; `id` is accepted but unused; 404 for an empty result |

Stack: Python, FastAPI, Pydantic, PostgreSQL and psycopg2.
Concepts: dataclasses, parameterized queries, joins, aggregation, typed response
models, nested serialization, dependency injection and connection lifecycle.

## Files

- `app.py`: routes and request-scoped connections.
- `database.py`: environment-based PostgreSQL connection factory, autocommit enabled.
- `models.py`: `User`, `Post` and `Feed` dataclasses.
- `schema.py`: Pydantic response models.
- `helpers.py`: record lookup, joined activity feed and popularity queries.
- `count_users.py`: standalone database count example using `DictCursor`;
  importing it does not open a connection.

## Run locally

From this directory, using a dedicated virtual environment:

```bash
pip install -r requirements.txt
uvicorn app:app --reload --env-file .env
```

Copy `.env.example` to a local `.env` and supply authorized database settings.
An existing local `.env` must be retained, not overwritten. `fastapi[all]` supplies
the dotenv support used by this command. Alternatively export all five `DB_*`
variables and omit `--env-file`. The connection factory itself reads only the
process environment.

The external schema requires `public."user"`, `public.post` and
`public.feed_action`. No schema migrations or source data are included.
For `count_users.py`, export the environment variables first, then run
`python count_users.py`.

## Restoration status

The API and SQL logic are preserved. Manual review remains for `Post.topic`
being optional while `PostGet.topic` requires a string, nullable database fields,
limits without positive bounds, and the nested dataclass serialization contract
in the selected runtime. Empty feed results intentionally retain the existing
404 response. Runtime API/database integration was not verified during the audit.

An unfinished duplicate lookup script and assignment instructions were moved
out of the public structure into the ignored local restoration archive. The
commented HTTP client and copied response texts were removed from `app.py`.
