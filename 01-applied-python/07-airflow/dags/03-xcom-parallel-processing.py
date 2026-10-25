

from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def generate_numbers():
    numbers = [5, 12, 3, 21, 8]

    print(numbers)

    return numbers


def find_sum(ti):
    numbers = ti.xcom_pull(
        task_ids="generate_numbers"
    )

    result = sum(numbers)

    print(f"Sum = {result}")

    return result


def find_max(ti):
    numbers = ti.xcom_pull(
        task_ids="generate_numbers"
    )

    max_number = max(numbers)

    print(f"Max = {max_number}")

    return max_number


def report(ti):
    total = ti.xcom_pull(
        task_ids="find_sum"
    )

    max_number = ti.xcom_pull(
        task_ids="find_max"
    )

    print(f"Sum = {total}")
    print(f"Max = {max_number}")

    return {
        "sum": total,
        "max": max_number,
    }


with DAG(
    dag_id="xcom_parallel_processing",
    description="Parallel processing and result aggregation with XCom",
    schedule=None,
    start_date=datetime(2026, 10, 5),
    catchup=False,
    tags=["practice", "xcom"],
) as dag:

    generate_numbers_task = PythonOperator(
        task_id="generate_numbers",
        python_callable=generate_numbers,
    )

    find_sum_task = PythonOperator(
        task_id="find_sum",
        python_callable=find_sum,
    )

    find_max_task = PythonOperator(
        task_id="find_max",
        python_callable=find_max,
    )

    report_task = PythonOperator(
        task_id="report",
        python_callable=report,
    )

    generate_numbers_task >> [
        find_sum_task,
        find_max_task,
    ] >> report_task
