# load/load.py

from utils.db_connection import get_engine
import pandas as pd

def load_to_postgres(df, table_name):
    engine = get_engine()
    print(f"\n🔍 Preview of '{table_name}' DataFrame:\n", df.head())
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Loaded '{table_name}' table into PostgreSQL.")

# --- Runner Function ---
def run_pipeline(final_df, customer_df, product_df, sales_df):
    print("🚀 Starting ETL Pipeline...\n")

    load_to_postgres(customer_df, "customer")
    load_to_postgres(product_df, "product")
    load_to_postgres(sales_df, "sales")
    load_to_postgres(final_df, "ecommerce_data")

    print("\n✅ ETL Pipeline completed successfully.")
