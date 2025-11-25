from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'yuksel',
    'depends_on_past': False,
    'email': ['admin@vektra.ai'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 2. DAG TANIMI
with DAG(
    'vektra_knowledge_base_update',
    default_args=default_args,
    description='Vektra AI - Kurumsal Hafıza Güncelleme Hattı',
    schedule_interval=None, 
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['vektra', 'rag', 'ai'],
) as dag:

    # 3. GÖREVLER (TASKS)
    t1_check_env = BashOperator(
        task_id='check_environment',
        bash_command='echo "Vektra AI Pipeline Başlatılıyor... PYTHONPATH: $PYTHONPATH"'
    )

    # GÖREV 2: Veri Sindirimi 
    t2_ingestion = BashOperator(
        task_id='run_ingestion',
        bash_command='export PYTHONPATH=$PYTHONPATH:/opt/airflow && python -m src.ingestion'
    )

    # GÖREV 3: Vektör Veritabanı Güncelleme 
    t3_vector_store = BashOperator(
        task_id='update_vector_store',
        bash_command='export PYTHONPATH=$PYTHONPATH:/opt/airflow && python -m src.vector_store'
    )

    # 4. SIRALAMA 
    t1_check_env >> t2_ingestion >> t3_vector_store