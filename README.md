# Supply Chain Dashboard and Data Analysis Project
## Overview

This project demonstrates a real-time dashboard for monitoring supply chain performance and key metrics. The dashboard helps analyze the efficiency of the order processing, shipping, and delivery processes. By simulating a business process with DAGs in Airflow, we automated the data generation and updating steps, allowing for real-time analysis and reporting.

The dashboard provides insights into:

- **Order Status Distribution**: Track the status of orders (Delivered, In Transit, Returned, Damaged) and identify trends.
- **Average Delivery Time**: See how quickly orders are being delivered and monitor delays.
- **Cost vs. Delivery Time**: Analyze the relationship between the cost of an order and the time it takes for delivery.
- **Key Performance Indicators (KPIs)**: Overall metrics including total orders, average delivery time, and total revenue.

## Automated Data Processing with Airflow

By using Airflow DAGs, we automated the data pipeline:
- The DAG simulates business processes and generates updated data on supply chain orders.
- Data aggregation and analysis are performed using Python and Pandas.
- The results are saved and updated regularly, ensuring real-time access to the latest metrics.

## Generated Report

Using the simulated and aggregated data, a detailed report was created to summarize the findings and insights. You can find the generated report [here](supply_chain_analysis_report.txt).

## Dashboard

For a visual representation of the data, a dashboard was created using Tableau (or another visualization tool). It provides an interactive view of the key metrics. You can see a sample image of the dashboard below:

![Supply Chain Dashboard](image_file_path.png)

## How to Use

- **DAG Script**: The DAG script used for automating data updates can be found [here](supply_chain_etl.py).
- **Python Reporting Script**: The data aggregation and reporting Python script can be found [here](supply_chain_reporting.py).
- **CSV Data**: Sample data files are also provided for further analysis or testing.

## License

This project is open-source and available for collaboration. Feel free to clone, modify, and contribute!
"""
