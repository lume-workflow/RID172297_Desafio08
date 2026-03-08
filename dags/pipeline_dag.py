from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

# ============================================================
# CONFIGURAÇÃO DO DAG
# ============================================================

default_args = {
    'owner': 'lume',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    dag_id='pipeline_medallion',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False,
)

# ============================================================
# CAMINHOS DAS CAMADAS
# ============================================================

BRONZE = '/opt/airflow/data/bronze'
PRATA  = '/opt/airflow/data/prata'
OURO   = '/opt/airflow/data/ouro'

# ============================================================
# TAREFA 1 — Bronze: carregar dados brutos
# ============================================================

def upload_raw_data_to_bronze():
    origem  = os.path.join(BRONZE, 'raw_data.csv')
    destino = os.path.join(BRONZE, 'bronze_data.csv')
    df = pd.read_csv(origem)
    df.to_csv(destino, index=False)
    print(f'Bronze: {len(df)} registros carregados.')

# ============================================================
# TAREFA 2 — Prata: limpar os dados
# ============================================================

def process_bronze_to_silver():
    df = pd.read_csv(os.path.join(BRONZE, 'bronze_data.csv'))

    # Remove registros com campos essenciais nulos
    df = df.dropna(subset=['name', 'email', 'date_of_birth'])

    # Remove emails sem "@"
    df = df[df['email'].apply(lambda x: '@' in str(x))]

    # Calcula a idade
    hoje = datetime.now()
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    df['age'] = df['date_of_birth'].apply(
        lambda x: hoje.year - x.year - ((hoje.month, hoje.day) < (x.month, x.day))
    )

    df.to_csv(os.path.join(PRATA, 'silver_data.csv'), index=False)
    print(f'Prata: {len(df)} registros após limpeza.')

# ============================================================
# TAREFA 3 — Ouro: agregar por faixa etária e status
# ============================================================

def process_silver_to_gold():
    df = pd.read_csv(os.path.join(PRATA, 'silver_data.csv'))

    # Define as faixas etárias
    bins   = list(range(0, 121, 10))
    labels = [f'{i+1}-{i+10}' for i in range(0, 120, 10)]
    df['faixa_etaria'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    # Agrega por faixa etária e status
    gold = df.groupby(['faixa_etaria', 'subscription_status']).size().reset_index(name='total_usuarios')

    gold.to_csv(os.path.join(OURO, 'gold_data.csv'), index=False)
    print(f'Ouro: {len(gold)} grupos gerados.')

# ============================================================
# DEFINIÇÃO DAS TAREFAS NO AIRFLOW
# ============================================================

tarefa_bronze = PythonOperator(
    task_id='carregar_bronze',
    python_callable=upload_raw_data_to_bronze,
    dag=dag,
)

tarefa_prata = PythonOperator(
    task_id='processar_prata',
    python_callable=process_bronze_to_silver,
    dag=dag,
)

tarefa_ouro = PythonOperator(
    task_id='processar_ouro',
    python_callable=process_silver_to_gold,
    dag=dag,
)

# Define a ordem de execução
tarefa_bronze >> tarefa_prata >> tarefa_ouro