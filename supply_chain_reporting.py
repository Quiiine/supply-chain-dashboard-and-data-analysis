import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_and_aggregate_data(**kwargs):
    
    csv_file = '/tmp/supply_chain_data_transformed.csv'
    
  
    df = pd.read_csv(csv_file)
    
    
    total_orders = df['Order ID'].nunique()
    
    avg_cost = df['Cost'].mean()
    
  
    avg_delivery_time_by_status = df.groupby('Status')['Delivery Time (Days)'].mean().reset_index()

    order_count_by_status = df.groupby('Status')['Order ID'].count().reset_index(name='Count')

    delayed_orders = len(df[df['Delivery Time (Days)'] > 10])
    percent_delayed_orders = (delayed_orders / total_orders) * 100

    returned_orders = len(df[df['Status'] == 'Returned'])
    damaged_orders = len(df[df['Status'] == 'Damaged'])
    percent_returned = (returned_orders / total_orders) * 100
    percent_damaged = (damaged_orders / total_orders) * 100
    
    df['Profit'] = df['Cost'] * 0.2
    total_profit = df['Profit'].sum()
    avg_profit_by_status = df.groupby('Status')['Profit'].mean().reset_index(name='Average Profit')
    
    max_delivery_time = df['Delivery Time (Days)'].max()
    min_delivery_time = df['Delivery Time (Days)'].min()
    avg_delivery_time = df['Delivery Time (Days)'].mean()
    
    delayed_orders_count = len(df[df['Delivery Time (Days)'] > 10])
    percent_over_target_time = (delayed_orders_count / total_orders) * 100
    
    report_data = {
        'Metric': [
            'Total Orders', 
            'Average Cost', 
            'Total Profit', 
            'Max Delivery Time', 
            'Min Delivery Time', 
            'Average Delivery Time',
            'Percent of Delayed Orders ( > 10 days)',
            'Percent of Returned Orders',
            'Percent of Damaged Orders',
            'Percent Over Target Delivery Time'
        ],
        'Value': [
            total_orders, 
            avg_cost, 
            total_profit, 
            max_delivery_time, 
            min_delivery_time, 
            avg_delivery_time,
            percent_delayed_orders,
            percent_returned,
            percent_damaged,
            percent_over_target_time
        ]
    }
    
    df_report = pd.DataFrame(report_data)
    
    report_file = '/tmp/supply_chain_advanced_report.csv'
    df_report.to_csv(report_file, index=False)
    
    print(f"Advanced report saved to {report_file}")
    
    return report_file

def save_report_info(**kwargs):
    ti = kwargs['ti']
    report_file = ti.xcom_pull(task_ids='load_and_aggregate_data')
    
    print(f"Report file generated at: {report_file}")

with DAG('supply_chain_advanced_reporting', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    load_and_aggregate_data = PythonOperator(
        task_id='load_and_aggregate_data',
        python_callable=load_and_aggregate_data,
    )
    
    save_report_info = PythonOperator(
        task_id='save_report_info',
        python_callable=save_report_info,
    )

    load_and_aggregate_data >> save_report_info
