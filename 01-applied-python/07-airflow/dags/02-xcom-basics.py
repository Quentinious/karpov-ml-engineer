
from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def push_xcom(ti):
    ti.xcom_push(
        key="sample_xcom_key",
        value="xcom test",
    )


def retrieve_xcom(ti):
    value = ti.xcom_pull(
        key="sample_xcom_key",
        task_ids="push_xcom",
    )

    print(value)


with DAG(
    dag_id="xcom_basics",
    description="Explicit XCom push and pull example",
    schedule=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["practice", "xcom"],
    default_args={
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    push_task = PythonOperator(
        task_id="push_xcom",
        python_callable=push_xcom,
    )

    retrieve_task = PythonOperator(
        task_id="retrieve_xcom",
        python_callable=retrieve_xcom,
    )

    push_task >> retrieve_task
