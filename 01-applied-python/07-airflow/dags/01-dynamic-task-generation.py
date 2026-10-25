

from datetime import datetime, timedelta
from textwrap import dedent

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator


def print_context(**kwargs):
    print(kwargs)
    print(f"Task number is: {kwargs.get('task_number')}")
    print(kwargs.get("ds"))

    return "Whatever you return gets printed in the logs"


with DAG(
    dag_id="dynamic_task_generation",
    description="Dynamic generation of Bash and Python tasks",
    schedule=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["practice", "dynamic-tasks"],
    default_args={
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    start = EmptyOperator(task_id="start")

    wait_for_bash_tasks = EmptyOperator(
        task_id="wait_for_all_bash_tasks"
    )

    finish = EmptyOperator(task_id="finish")

    for i in range(10):
        bash_task = BashOperator(
            task_id=f"print_number_{i}",
            bash_command='echo "doing magic $NUMBER"',
            env={"NUMBER": str(i)},
        )

        bash_task.doc_md = dedent(
            f"""
            #### Task {i}

            Dynamically generated Bash task.
            """
        )

        start >> bash_task >> wait_for_bash_tasks



    for i in range(20):
        python_task = PythonOperator(
            task_id=f"print_context_{i}",
            python_callable=print_context,
            op_kwargs={"task_number": i},
        )

        wait_for_bash_tasks >> python_task >> finish
