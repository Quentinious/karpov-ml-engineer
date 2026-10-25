

from datetime import datetime, timedelta

from airflow.sdk import DAG, Variable
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import (
    BranchPythonOperator,
    PythonOperator,
)


STARTML_TASK_ID = "startml_description"
OTHER_COURSE_TASK_ID = "other_course_description"


def print_variable():
    value = Variable.get("is_startml")

    print(f"is_startml = {value}")


def choose_course():
    """Choose the next task based on the is_startml Airflow Variable."""
    is_startml = Variable.get("is_startml")

    if is_startml == "True":
        return STARTML_TASK_ID

    return OTHER_COURSE_TASK_ID


def describe_startml():
    print("StartML is a starter course for ambitious people")


def describe_other_course():
    print("Not a StartML course, sorry")


with DAG(
    dag_id="branching_with_variable",
    description="Conditional DAG branching based on an Airflow Variable",
    schedule=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["practice", "branching"],
    default_args={
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    before_branching = EmptyOperator(
        task_id="before_branching"
    )

    print_var = PythonOperator(
        task_id="print_variable",
        python_callable=print_variable,
    )

    branching = BranchPythonOperator(
        task_id="determine_course",
        python_callable=choose_course,
    )

    startml_task = PythonOperator(
        task_id=STARTML_TASK_ID,
        python_callable=describe_startml,
    )

    other_course_task = PythonOperator(
        task_id=OTHER_COURSE_TASK_ID,
        python_callable=describe_other_course,
    )

    after_branching = EmptyOperator(
        task_id="after_branching",
        trigger_rule="none_failed_min_one_success",
    )

    before_branching >> print_var >> branching

    branching >> [
        startml_task,
        other_course_task,
    ]

    [
        startml_task,
        other_course_task,
    ] >> after_branching
