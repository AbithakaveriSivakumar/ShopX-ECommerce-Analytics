# ADMM Case Study - ShopX E-Commerce Analytics

## Project Overview

This project implements an ETL pipeline for e-commerce order fulfilment
and delivery analytics.

The project extracts data from SAP-related source datasets, performs
data cleaning and transformation using Python, loads the processed
data into a MySQL data warehouse, and prepares the data for Power BI
analytics and dashboard development.

---

## Technologies Used

- Python
- Pandas
- OpenPyXL
- MySQL
- SQL
- Power BI
- GitHub

---

## Project Workflow

Source SAP Dataset
        |
        v
Data Extraction
        |
        v
Data Cleaning and Validation
        |
        v
Data Transformation
        |
        v
Order Processing Time Calculation
        |
        v
Delivery Analytics
        |
        v
MySQL Data Warehouse
        |
        v
Power BI Dashboard

---

## Source Dataset

The project uses an SAP-based e-commerce dataset containing data
from multiple SAP tables.

The source dataset is not included in this repository because it
may contain restricted or training-provided data.

The required file is:

SAP-DataSet.xlsx

Place the dataset in the same folder as `etl_shopx.py` before running
the ETL script.

---

## SAP Source Tables

The ETL process uses the following SAP source tables:

- KNA1 - Customer data
- LFA1 - Carrier data
- VBAK - Sales order header data
- VBAP - Sales order item data
- LIKP - Delivery header data
- LIPS - Delivery item data
- VTTK - Shipment data
- VTTP - Shipment item data

---

## ETL Process

### 1. Data Extraction

The source Excel workbook is loaded using Pandas and the required
SAP worksheets are extracted.

### 2. Data Cleaning and Validation

The data is checked for:

- Missing values
- Duplicate records
- Invalid quantities
- Invalid or inconsistent dates
- Required key fields

### 3. Data Transformation

The extracted datasets are transformed into analytical structures
required for the data warehouse.

### 4. Order Processing Time

Order processing time is calculated based on the relevant order and
shipment dates.

### 5. Delivery Analytics

Delivery delay is calculated by comparing the actual delivery date
with the expected delivery date.

### 6. MySQL Data Warehouse

The transformed data is loaded into the `shopx_dw` MySQL database.

Main tables include:

- customers
- carriers
- orders
- order_items
- shipments
- shipment_items
- delivery_analytics

---

## Power BI Dashboard

The Power BI dashboard contains the following KPIs and charts:

### KPI Cards

- Average Delivery Delay
- Average Order Processing Days
- Late Delivery Rate

### Charts

- Delivery Delay Trend
- Delivery Delay by Carrier

---

## Dashboard Results

The dashboard produced the following results:

- Average Delivery Delay: approximately 1.15 days
- Average Order Processing Days: approximately 7.20 days
- Late Delivery Rate: 100%

Carrier-level average delivery delay was also analyzed for the
available carriers.

---

## Project Structure

```text
ADMM_CaseStudy/
│
├── etl_shopx.py
├── requirements.txt
├── README.md
├── .gitignore
└── SAP-DataSet.xlsx