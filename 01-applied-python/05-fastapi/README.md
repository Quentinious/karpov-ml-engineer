# FastAPI database lookups

A small API validates user input and retrieves PostgreSQL records.

| Endpoint | Behavior |
| --- | --- |
| `POST /user/validate` | Validate name, surname, age and registration date; return a confirmation string |
| `GET /user/{id}` | Retrieve gender, age and city, or return 404 |
| `GET /post/{id}` | Retrieve ID, text and topic through `PostResponse`, or return 404 |

Stack: Python, FastAPI, Pydantic, PostgreSQL and psycopg2.
Concepts: request/response models, typed path parameters, parameterized SQL,
HTTP exceptions and dependency injection with connection cleanup.
The POST endpoint validates data; it does not insert a user into the database.

## Run locally

From this directory, using a dedicated virtual environment:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Before starting, export `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and
`DB_PASSWORD` in the process environment. `.env.example` contains placeholders.
The application does not load `.env` automatically: either export those values or
install `python-dotenv` and run `uvicorn app:app --reload --env-file .env`.
Keep the local `.env` ignored by Git.

Requires an authorized PostgreSQL database with `"user"` and `post` tables.
Dependencies retain the original unpinned form; runtime reproduction and behavior
with nullable database fields require review. No external database was contacted
in the repository audit.
