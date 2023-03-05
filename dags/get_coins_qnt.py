from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import binance_bot.create_account as ca


with DAG(dag_id="geting_coins_qnt",
         start_date=datetime(2022,1,1),
         schedule_interval="@daily",
         catchup=False) as dag:

    def helloWorld():
        ca.getting_qnt_coins()

    task1 = PythonOperator(
        task_id="geting_qnt",
        python_callable=helloWorld)

task1

if __name__ == '__main__':
    dag.test()