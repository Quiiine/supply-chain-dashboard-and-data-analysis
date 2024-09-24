from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import random

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_data(**kwargs):
    import pandas as pd
    from datetime import datetime, timedelta
    import random
    
    # Количество заказов для генерации
    num_orders = 1000
    start_date = datetime(2023, 1, 1)
    
    # Список для хранения данных
    data = []
    
    for i in range(1, num_orders + 1):
        order_id = i
        order_received = start_date + timedelta(days=random.randint(0, 180))
        processing_time = timedelta(days=random.randint(1, 5))
        shipping_time = timedelta(days=random.randint(1, 7))
        delivery_time = timedelta(days=random.randint(1, 10))

        order_processed = order_received + processing_time
        shipment_sent = order_processed + shipping_time
        order_delivered = shipment_sent + delivery_time

        cost = round(random.uniform(50, 500), 2)
        current_date = datetime.now()

        # Определение статуса заказа на основе текущей даты
        if order_delivered <= current_date:
            status = random.choices(
                ['Delivered', 'Returned', 'Damaged'], 
                weights=[0.8, 0.1, 0.1], 
                k=1
            )[0]
        elif shipment_sent <= current_date < order_delivered:
            status = 'In Transit'
        elif order_processed <= current_date < shipment_sent:
            status = 'Shipped'
        elif order_received <= current_date < order_processed:
            status = 'Processing'
        else:
            status = 'Order Received'

        data.append({
            'Order ID': order_id,
            'Order Received': order_received.date(),
            'Order Processed': order_processed.date(),
            'Shipment Sent': shipment_sent.date(),
            'Order Delivered': order_delivered.date(),
            'Cost': cost,
            'Status': status
        })

    df = pd.DataFrame(data)
    df.to_csv('/tmp/supply_chain_data.csv', index=False)
    print('Данные успешно сгенерированы и сохранены.')

def transform_data(**kwargs):
    df = pd.read_csv('/tmp/supply_chain_data.csv')
    df['Delivery Time (Days)'] = (pd.to_datetime(df['Order Delivered']) - pd.to_datetime(df['Order Received'])).dt.days
    df.to_csv('/tmp/supply_chain_data_transformed.csv', index=False)
    print('Данные успешно трансформированы.')

def load_data(**kwargs):
    print('Данные готовы для анализа.')

with DAG('supply_chain_etl', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    generate = PythonOperator(
        task_id='generate_data',
        python_callable=generate_data,
    )

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    generate >> transform >> load
