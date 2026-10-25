# SQL and PostgreSQL

Two query collections analyze users, posts and their interactions:

- `01-basic-queries.sql`: samples, distinct topics, user filters, country and
  experiment-group statistics, long post topics and rankings.
- `02-joins-and-analytics.sql`: recent likes from Omsk users, city-level views
  for a selected cohort/date/topic, and post popularity with latest activity.

Stack: PostgreSQL and SQL. Concepts: `WHERE`, `DISTINCT`, boolean precedence,
`GROUP BY`, `HAVING`, aggregates, `ORDER BY`, `LIMIT`, joins and date filtering.
The external schema contains `public."user"`, `post` and `feed_action`; no
schema creation scripts, source data or database credentials are included.
Run individual queries against an authorized database with those tables.

Status: restored solutions and one grouping example (country/experiment group).
Original assignment text was replaced by comments describing the actual SQL.
Query logic is preserved, including these review points:

- In the combined country/group/city filter, Minsk satisfies the `OR` branch
  regardless of country because `AND` takes precedence.
- Samples without `ORDER BY` do not establish the first or smallest ID.
- Topic and country rankings return all qualifying rows, not a fixed top-N.
- Voronezh age ties have no experiment-group tie-breaker.
- The city view query includes only cities with matching events, excluding zeros;
  ties for the minimum are not resolved explicitly.

These are not certified final answers to the original course tasks. Queries were
not run against the external database during the repository audit.
