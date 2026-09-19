import pandas as pd

file_path = "SAP-DataSet.xlsx"

kna1 = pd.read_excel(file_path, sheet_name="KNA1")
lfa1 = pd.read_excel(file_path, sheet_name="LFA1")
vbak = pd.read_excel(file_path, sheet_name="VBAK")
vbap = pd.read_excel(file_path, sheet_name="VBAP")
likp = pd.read_excel(file_path, sheet_name="LIKP")
lips = pd.read_excel(file_path, sheet_name="LIPS")
vttk = pd.read_excel(file_path, sheet_name="VTTK")
vttp = pd.read_excel(file_path, sheet_name="VTTP")

print("Data Loaded Successfully")


def basic_clean(df):
    df = df.dropna(how="all")

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df


kna1 = basic_clean(kna1)
lfa1 = basic_clean(lfa1)
vbak = basic_clean(vbak)
vbap = basic_clean(vbap)
likp = basic_clean(likp)
lips = basic_clean(lips)
vttk = basic_clean(vttk)
vttp = basic_clean(vttp)

print("Basic Cleaning Completed")



customers = kna1[["Customer ID","Customer Name", "Country","Region","City","Postal Code", "Street Address", "Phone Number","Email Address"]].copy()

customers.columns = ["customer_id","customer_name","country","region","city","postal_code","street_address","phone","email"]

customers = customers.dropna(subset=["customer_id"])

customers = customers.drop_duplicates(subset=["customer_id"])

print(customers.head())



carriers = lfa1[["Vendor Number", "Vendor Name","Country","Region","City","Postal Code","Street Address","Phone Number","Email Address"]].copy()

carriers.columns = ["carrier_id","carrier_name","country","region","city","postal_code","street_address","phone","email"]

carriers = carriers.dropna(subset=["carrier_id"])

carriers = carriers.drop_duplicates(subset=["carrier_id"])



orders = vbak[["Sales Document","Order Date","Customer ID","Order Status"]].copy()

orders.columns = ["order_id","order_date","customer_id","order_status"]

orders["order_date"] = pd.to_datetime(orders["order_date"],errors="coerce")

orders = orders.dropna(subset=["order_id", "customer_id", "order_date"])

orders = orders.drop_duplicates(subset=["order_id"])




order_items = vbap[["Sales Document","Item Number","Material Number","Quantity","Net Price","Delivery Date"]].copy()

order_items.columns = ["order_id","item_no","material_id","quantity","unit_price","expected_delivery_date"]

order_items["quantity"] = pd.to_numeric(order_items["quantity"],errors="coerce")

order_items["unit_price"] = pd.to_numeric(order_items["unit_price"],errors="coerce")

order_items["expected_delivery_date"] = pd.to_datetime(order_items["expected_delivery_date"],errors="coerce")

order_items = order_items.dropna(subset=["order_id", "material_id"])

order_items = order_items[order_items["quantity"] > 0]


shipments = vttk[["Shipment Number","Shipment Date","Sales Document","Carrier","Shipment Status"]].copy()

shipments.columns = ["shipment_id","shipment_date","order_id","carrier","shipment_status"]

shipments["shipment_date"] = pd.to_datetime(shipments["shipment_date"],errors="coerce")

shipments = shipments.dropna(subset=["shipment_id", "order_id"])

shipments = shipments.drop_duplicates(subset=["shipment_id"])


shipment_items = vttp[["Shipment Number","Item Number","Material Number","Shipped Quantity","Shipment Date","Item Status"]].copy()

shipment_items.columns = ["shipment_id","item_no","material_id","shipped_quantity","shipment_date","item_status"]

shipment_items["shipment_date"] = pd.to_datetime(shipment_items["shipment_date"],errors="coerce")

shipment_items["shipped_quantity"] = pd.to_numeric(shipment_items["shipped_quantity"],errors="coerce")


deliveries = lips[["Delivery Number","Delivery Date","Sales Document"]].copy()

deliveries.columns = ["delivery_id","actual_delivery_date","order_id"]

deliveries["actual_delivery_date"] = pd.to_datetime(deliveries["actual_delivery_date"],errors="coerce")

deliveries = deliveries.dropna(subset=["delivery_id", "actual_delivery_date"])

deliveries = deliveries.drop_duplicates(subset=["delivery_id"])



order_processing = pd.merge(
        orders[["order_id", "order_date"]],
        shipments[["order_id", "shipment_date"]],
        on="order_id",
        how="left"
)

order_processing["order_processing_days"] = (
    order_processing["shipment_date"]-order_processing["order_date"]
).dt.days


shipments = pd.merge(shipments,order_processing[["order_id", "order_processing_days"]],on="order_id", how="left")


expected_delivery = (
    order_items
    .groupby("order_id")["expected_delivery_date"]
    .max()
    .reset_index()
)

delivery_analytics = pd.merge(
    deliveries[
        [
            "order_id",
            "actual_delivery_date"
        ]
    ],
    expected_delivery,
    on="order_id",
    how="inner"
)

delivery_analytics = pd.merge(
    delivery_analytics,
    shipments[["shipment_id","order_id","shipment_date","carrier"]],
    on="order_id",
    how="left")


delivery_analytics["delivery_delay"] = (
    delivery_analytics["actual_delivery_date"]-
    delivery_analytics["expected_delivery_date"]
).dt.days

delivery_analytics["on_time"] = ( 
    delivery_analytics["delivery_delay"] <= 0
).astype(int)

delivery_analytics["delay_reason"] = None


print("\nFinal Row Counts:")
print("Orders:", len(orders))
print("Order Items:", len(order_items))
print("Customers:", len(customers))
print("Carriers:", len(carriers))
print("Shipments:", len(shipments))
print("Shipment Items:", len(shipment_items))
print("Deliveries:", len(deliveries))

print("\nETL Cleaning & Transformation Completed Successfully")




import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="shopx_dw"
)

cursor = conn.cursor()

print("Connected to MySQL")


for _, row in customers.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO customers
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["customer_id"],
        row["customer_name"],
        row["country"],
        row["region"],
        row["city"],
        row["postal_code"],
        row["street_address"],
        row["phone"],
        row["email"]
    ))

conn.commit()

print("Customers Loaded")

for _, row in carriers.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO carriers
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        int(row["carrier_id"]),
        row["carrier_name"],
        row["country"],
        row["region"],
        row["city"],
        row["postal_code"],
        row["street_address"],
        row["phone"],
        row["email"]
    ))

conn.commit()

print("Carriers Loaded")


for _, row in orders.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO orders
        VALUES (%s,%s,%s,%s)
    """, (
        int(row["order_id"]),
        row["order_date"].date(),
        row["customer_id"],
        row["order_status"]
    ))

conn.commit()

print("Orders Loaded")


for _, row in order_items.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO order_items
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        int(row["order_id"]),
        int(row["item_no"]),
        row["material_id"],
        float(row["quantity"]),
        float(row["unit_price"]),
        row["expected_delivery_date"].date()
    ))

conn.commit()

print("Order Items Loaded")

for _, row in shipments.iterrows():

    processing_days = row["order_processing_days"]

    if pd.isna(processing_days):
        processing_days = None
    else:
        processing_days = int(processing_days)

    cursor.execute("""
        INSERT IGNORE INTO shipments
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        int(row["shipment_id"]),
        int(row["order_id"]),
        row["carrier"],
        row["shipment_date"].date(),
        row["shipment_status"],
        processing_days
    ))

conn.commit()

print("Shipments Loaded")


for _, row in shipment_items.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO shipment_items
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        int(row["shipment_id"]),
        int(row["item_no"]),
        row["material_id"],
        float(row["shipped_quantity"]),
        row["shipment_date"].date(),
        row["item_status"]
    ))

conn.commit()

print("Shipment Items Loaded")

for _, row in delivery_analytics.iterrows():

    cursor.execute("""
        INSERT IGNORE INTO delivery_analytics
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        int(row["order_id"]),
        int(row["shipment_id"]),
        row["expected_delivery_date"].date(),
        row["actual_delivery_date"].date(),
        int(row["delivery_delay"]),
        int(row["on_time"]),
        row["delay_reason"]
    ))

conn.commit()

print("Delivery Analytics Loaded")