

from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import PythonOperator


def get_active_user():
    """Return the user with the largest number of likes."""
    from psycopg2.extras import RealDictCursor

    postgres = PostgresHook(
        postgres_conn_id="startml_feed"
    )

    with postgres.get_conn() as conn:
        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                """
                SELECT
                    f.user_id,
                    COUNT(*) AS likes_count
                FROM feed_action AS f
                WHERE f.action = 'like'
                GROUP BY f.user_id
                ORDER BY likes_count DESC
                LIMIT 1
                """
            )

            result = cursor.fetchone()

    return result


def print_result(ti):
    """Print the query result received through XCom."""
    result = ti.xcom_pull(
        task_ids="postgres_query",
        key="return_value",
    )

    print(result)


with DAG(
    dag_id="postgres_hook_example",
    description="PostgreSQL query through an Airflow Connection",
    schedule=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["practice", "postgres"],
    default_args={
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    postgres_query = PythonOperator(
        task_id="postgres_query",
        python_callable=get_active_user,
    )

    print_operator = PythonOperator(
        task_id="print_result",
        python_callable=print_result,
        doc_md="Print the PostgreSQL query result received through XCom.",
    )

    postgres_query >> print_operator
