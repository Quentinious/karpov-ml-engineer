# Apache Airflow workflows

Five independent practice DAGs demonstrate orchestration using Airflow 3 authoring
imports (`airflow.sdk`) and the standard/PostgreSQL providers.

| File in `dags/` | Workflow and concepts |
| --- | --- |
| `01-dynamic-task-generation.py` | Start -> 10 Bash tasks -> barrier -> 20 Python tasks -> finish; parse-time task generation, context, retries and fan-in |
| `02-xcom-basics.py` | Push a value under a custom XCom key and retrieve it downstream |
| `03-xcom-parallel-processing.py` | Generate a list -> sum/max in parallel -> report; return-value XCom and fan-in |
| `04-postgres-hook.py` | Find the user who gave the most likes -> print result; `PostgresHook`, Connection and XCom |
| `05-branching-with-variable.py` | Read a Variable -> choose one message -> join; branching and skipped tasks |

Stack: Python, Apache Airflow 3, `apache-airflow-providers-standard`,
`apache-airflow-providers-postgres` and psycopg2. No exact Airflow/provider versions
were recorded. These dependencies belong in a separately managed Airflow runtime,
not the API environments. A working Airflow deployment is required to schedule DAGs.
The PostgreSQL example uses a psycopg2 `RealDictCursor`; check the provider's driver
selection when configuring an environment that also contains psycopg 3.

## External configuration

- Configure the Airflow Connection `startml_feed` with authorized PostgreSQL
  settings. That identifier is a reference, not a credential. The query uses
  `feed_action` from the connection's search path.
- Set the Airflow Variable `is_startml`. Only the exact string `True` selects
  `startml_description`; every other value selects `other_course_description`.
  A missing variable raises an error. It is read at task execution time.
- DAG 03 has `schedule=None`; the other examples run daily with `catchup=False`.

The parallel fan-in tasks require all upstream tasks to succeed. The branching
join uses `none_failed_min_one_success`, allowing the unselected branch to be
skipped. These dependency choices are consistent with the intended graphs.

No credentials, deployment files or course infrastructure were found here.
The first DAG contains generic tutorial-style code; authorship and any required
attribution for the examples must be confirmed before publication. No Airflow
runtime is installed in the project environment, so scheduling and provider
integration have not been verified.

References: [Airflow 3 authoring interface](https://airflow.apache.org/docs/task-sdk/stable/),
[branching and trigger rules](https://airflow.apache.org/docs/apache-airflow/3.0.3/core-concepts/dags.html),
[PostgresHook](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/hooks/postgres/index.html).
