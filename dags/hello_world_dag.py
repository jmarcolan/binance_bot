from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import binance_bot.create_bot as cb


with DAG(dag_id="hello_world_dag",
         start_date=datetime(2022,1,1),
         schedule_interval=timedelta(seconds=20),
         catchup=False) as dag:

    def helloWorld():
        cb.test_get_all()

    task1 = PythonOperator(
        task_id="lol_go",
        python_callable=helloWorld)

task1

if __name__ == '__main__':
    dag.test()